from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from botasaurus.browser import browser
from botasaurus.request import request, Request
from botasaurus.soupify import soupify
import time
import json

@browser
def scrape_hotes(driver, url):
    try:
        # Navigate to URL
        print('Navigating to URL:', url)
        driver.get(url)
        print('Page loaded successfully')
        
        # Wait a bit for navigation to start
        time.sleep(3)
        
        # Try to handle consent dialog using JavaScript
        try:
            # Look for and click "Got it" button using JavaScript
            got_it_clicked = driver.run_js("""
                const dialogs = document.querySelectorAll('[role="dialog"]');
                for (const dialog of Array.from(dialogs)) {
                    const button = dialog.querySelector('.RxNS-button-content');
                    if (button && button.textContent && button.textContent.includes('Got it')) {
                        button.click();
                        return true;
                    }
                }
                return false;
            """)
            
            if got_it_clicked:
                print('Accepted consent dialog with "Got it" button.')
            else:
                print('Dialog found but "Got it" button not found.')
        except Exception as e:
            print('Consent dialog not found or error handling it:', e)
        
        # Wait a bit after potential consent dialog
        time.sleep(5)
        
        # Wait for search results to load
        try:
            driver.wait_for_element('section#resultWrapper')
        except:
            print('Search results wrapper not found, continuing anyway...')
        
        # Get total number of pages from pagination buttons
        page_count = driver.run_js("""
            // Look for pagination buttons to determine total pages
            const paginationButtons = document.querySelectorAll('.Joiu-buttons button[aria-label^="Page "]');
            let maxPage = 1;
            
            paginationButtons.forEach(button => {
                const ariaLabel = button.getAttribute('aria-label');
                if (ariaLabel) {
                    const pageMatch = ariaLabel.match(/Page (\\d+)/);
                    if (pageMatch) {
                        const pageNum = parseInt(pageMatch[1]);
                        if (pageNum > maxPage) {
                            maxPage = pageNum;
                        }
                    }
                }
            });
            
            return maxPage;
        """)
        
        print(f'Found {page_count} pages to scrape')
        
        all_results = []
        
        # Scrape each page
        for current_page in range(1, page_count + 1):
            print(f'Scraping page {current_page} of {page_count}')
            
            # If not the first page, navigate to the next page
            if current_page > 1:
                try:
                    # Click the "Next page" button
                    driver.wait_for_element('button[aria-label="Next page"]:not([disabled])')
                    driver.click('button[aria-label="Next page"]:not([disabled])')
                    
                    # Wait for the page to load by checking if the active page button has changed
                    # Use a simple loop to wait for page change
                    max_wait_time = 15  # seconds
                    wait_interval = 0.5  # seconds
                    waited_time = 0
                    
                    while waited_time < max_wait_time:
                        current_active_page = driver.run_js("""
                            const activeButton = document.querySelector('button[id="active"]');
                            if (activeButton) {
                                const ariaLabel = activeButton.getAttribute('aria-label');
                                const pageMatch = ariaLabel.match(/Page (\\d+)/);
                                return pageMatch ? parseInt(pageMatch[1]) : 0;
                            }
                            return 0;
                        """)
                        
                        if current_active_page == current_page:
                            print(f'Successfully navigated to page {current_page}')
                            break
                        
                        time.sleep(wait_interval)
                        waited_time += wait_interval
                    else:
                        print(f'Timeout waiting for page {current_page} to load')
                    
                    # Additional wait for content to load
                    time.sleep(3)
                except Exception as error:
                    print(f'Failed to navigate to page {current_page}:', error)
                    break  # Stop if we can't navigate to next page
            
            # Extract search results from current page
            page_results = driver.run_js("""
                const results = [];
                // Get all search result elements
                const hotelElements = document.querySelectorAll('section#resultWrapper .S0Ps .S0Ps-middleSection');
                hotelElements.forEach((hotelElement) => {
                    const hotelData = { name: '', providers: [] };
                    const nameElement = hotelElement.querySelector('.c9Hnq .c9Hnq-hotel-name');
                    if (nameElement) {
                        hotelData.name = nameElement.textContent || '';
                    }
                    const providerElements = hotelElement.querySelectorAll('.qSC7-pres-vertical >div >a');
                    providerElements.forEach((providerElement) => {
                        const providerData = {
                            url: providerElement.getAttribute('href') || '',
                        };
                        const priceElement = providerElement.querySelector('.hzpu-vertical-price');
                        if (priceElement) {
                            const price = priceElement.textContent || '';
                            providerData.price = price;
                        }
                        const providerLogoElement = providerElement.querySelector('img.afsH-provider-logo');
                        if (providerLogoElement) {
                            const providerLogo = providerLogoElement.getAttribute('src') || '';
                            providerData.logo = providerLogo;
                        }
                        hotelData.providers.push(providerData);
                    });
                    results.push(hotelData);
                });
                return results;
            """)
            
            all_results.extend(page_results)
            print(f'Scraped {len(page_results)} hotels from page {current_page}')
            
            # Add a small delay between pages to avoid being blocked
            if current_page < page_count:
                time.sleep(2)
        
        print(f'Total hotels scraped: {len(all_results)}')
        return all_results
        
    except Exception as error:
        print('Error in scrape_hotes:', error)
        return []

class ScrapeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        url = request.data.get('url')
        if not url:
            return Response({'error': 'Missing url parameter'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            hotels_data = scrape_hotes(url)
            
            # Check if results are empty
            if not hotels_data:
                return Response({'error': 'No hotels found'}, status=status.HTTP_404_NOT_FOUND)
            
            return Response({
                'hotels': hotels_data,
                'total_hotels': len(hotels_data)
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
