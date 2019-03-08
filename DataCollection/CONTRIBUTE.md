## Coding style
1. try to stick to **PEP-8** code guidelines
1. To keep the api surface as small as possible make functions and import private (using `_` prefix)

## Todo

[ ] After an error halfway through a given list, the code should be able to 
restart after the last successful  
[ ] When an api key hits it limits, the next possible key should be used  
[ ] Add tests to the package  
[ ] Add google api config to readme  
[ ] Add documentation on domain and getting started using documentation generation    
  *  **Implementation note** we could use [sphinx](http://www.sphinx-doc.org/en/stable/)    
  
[ ] Provide a better user experience with progress bar  
   * **Implementation note**: we could use the [tqdm package](https://github.com/tqdm/tqdm)  
     
[ ] Be able to rerun the scraping and only add the new finds
  * **Implementation note** requires a way to perform a delta, possible filter solution space using a last run date
  
 
   

   