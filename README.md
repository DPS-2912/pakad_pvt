Stage 1: Data Collection

    Code Access: The code for data collection is located under the "Data_Collection" tab.
    
    Tools & Environment: We employ automated browsers, specifically Selenium and tbselenium, for gathering data. This process is conducted over fiber and Starlink connections using both Firefox and Tor browsers.
    
    Master Code is code for main control machine and Data Collection code is for VMs
    
    Process Control: The master machine contains code that dictates which websites the Virtual Machines (VMs) should visit. These targeted websites are listed in the Tranco list, which should be stored in the same directory as the master code.
    
    VM Setup: Two VMs are set up on the master machine; one routes primarily through a fiber connection, while the other uses a Starlink connection. It's crucial to copy the Geckodriver and the specific version of the Tor browser to these VMs. If you're using separate machines instead of VMs, adjust the IP addresses in the master code accordingly.
    
    Data Collection Method: We utilize Docker containers to streamline the data collection process. Note that the Docker file should specify the versions of Geckodriver and the Tor browser being used.
    
    Browser Management: We restart the Tor and Firefox drivers and browsers for each session. While this extends the duration of data collection, it minimizes errors.
    
    Code Resilience: The code can handle minor network issues. It visits each website 2*n+1 times (where n is the batch number) before proceeding to the next. Both the batch number and the number of instances per webpage can be adjusted in the master code. Data, including screenshots and packet captures (pcaps), are stored in Docker storage. Ensure there's a method to transfer this data to the VM.
    
    Troubleshooting Tips: If you encounter errors, verify that the data is being captured correctly and that you're using the latest versions of Geckodriver and Tor browser. Also, consider adjusting the number of instances per batch if storage and RAM limitations are causing issues.

Stage 2: Data Processing

    Preprocessing: Data collected should be processed to extract timing, direction, and size information from packets/Tor cells, building upon previous website fingerprinting research.
    
    Attack and Defense Codes: The repository codes_all includes codes for attacks, aligning with methodologies used in prior research. Additionally, the code for defenses employed in our research is available at https://github.com/veichta/DeepSE-WF on GitHub.
    
    Data Details and Format: Comprehensive information about the data collected in our research can be found at this https://doi.org/10.5281/zenodo.10478854 link. All data formatting adheres to the standard time size*direction format.
