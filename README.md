# Overview
Wi-Form is a endeavour to map and give form to places’ WIFI signature. This is done through a reworked take on Wardriving, Warwalking, etc.

A mobile device with a GPS module and a WIFI module (with a monitor-mode capabilities) collect the WIFI probes sent by nearby devices. The data is then stored in a 3 dimensional table, where the X and Y are the latitude and longitude and the Z is the strength of the probe signal.

The data is outputted as a csv file that can be imported into a 3D program and viewed as a pointcloud. This is then processed though a surface reconstruction to get a solid mesh. More detail on this in the instruction section.

### Requirements
1. Python 3.x, and the following libraries:
    - Scrapy
    - Csv
    - Netaddr 
    - Serial
2. Airmon-ng
3. GPS module
4. Wifi adaptor with monitor-mode capabilities
5. Mobile device running Linux (Such as a Raspberry Pi, but any mobile Linux device should work)

### Installation
Download the repository, ether as a zip or clone it, and install the required python libraries. You can do this manually using pip install, or use the requirements.txt file while in the downloaded repository folder.
And install aircrack-ng, if you don't have it. 
```
git clone https://github.com/Wi-Form/Wi-Form
pip install -r requirements.txt
# And if needed #
sudo apt-get install aircrack-ng 
```

## Setup
Then we need to get the address of the GPS module and the WIFI adaptor. (If you don’t know how to do this see below) Take the address of the GPS module and inset into the code at the top where is say 
`GPSPATH = None` Change the None for the path to your module

The script is thought and tested as being used with a Raspberry Pi (or other arm devices) in headless mode with a ssh connecting to a phone. There is a bash script template at https://github.com/Wi-Form/Wi-bash/ that makes the process of using the script on headless devices alot less painfull.

### Find the GPS&WIFI module address
#### GPS
```
# With the GPS module unplugged open a terminal window and type
ls /dev/
# Then plug the module in and type
ls /dev/
# There should be a new address now – this is the module.
# Typically it is at “ttyACM(x)”, x being a number between 0 and 10.
ls /dev/ | grep ttyACM
# To make the output more manageable
```


#### WIFI adaptor
For the WIFI adaptor you simply use the command ` airmon-ng ` and look for your preferred adaptor.
Should be something like “wlan(x)”, but this can vary from distro to distro.
You can then start the WIFI adaptor in monitor mode using the start command in airmon-ng

```
# Find adaptor
airmon-ng
# Start adaptor in monitor mode
airmon-ng start wlan(x)
```


## Usage
The script takes in one mandatory argument (Capture interface) and two optional arguments (log output and output path)

Args:
   - -i (Capture interface)
   - -l (Output log in realtime)
   - -o (Path to output file – Default is the same path as the script)

Example:
` python main.py -i wlan0mon -l -o /home/user/Desktop `

This command will show collection of data in realtime and save the output file on the desktop.

## Post-processing / Making the mesh
<p align="center"><img src="https://wi-form.com/wp-content/uploads/2019/12/infographic-22-12-2019.png"/></p>
The process of making the pointcloud into a solid mesh a multiple stepped process. The process uses two programs to generate the mesh:

* Blender 2.7
* With the cvs importer plugin <a href="https://blenderartists.org/t/a-script-to-import-a-csv-file-and-create-meshes-for-blender-2-5x-or-later/501410">Link to plugin</a> 
* Meshmixer

Keep in mind this is an experimental process, so play around with the settings until you get something that you think works.

    1. Import to blender using the csv importer
    
    2. Export as DAE
    
    3. Open DAE in meshmixer
        Render->
        [*] Show Vertex Normals
    
    4. Filters->Point Set →
        [*] Compute Normals Neighbors 14
        [*] Flip Normals checked
    
    5. Filters->SamplingFilters->
        [*] Poisson-disk Samples: 5000 
        [*] Base Mesh Sampling Checked
    
    6. Filters->Point Set->Surface Reconstruction
        [*] Poisson Octree: 12
        [*] Solver: 7
    
    7. Filters->Remeshing->
        [*] LS3, 3 Iterations (default)
    
    8. Filters->Sampling->Vertex
        [*] Attrib Transfer Source: *.ply
        [*] Target: Poisson Mesh
    
    9. Transfer Geometry
        [*] Transfer Normal
    
    10. Filters->Cleaning-> 
        [*] Remove Duplicate Vertex
    
    11. Export as STL

## Sharing and contributing
If you get a form that you wanna share with others, you can head over to <a href="https://www.Wi-Form.com">Wi-Form.com</a> and upload your form as an .obj which will then be featured on the sites gallery.

#### Setting up your file
For preformence resons the form can have a maximum of 2500 faces. Usually the forms have alot more, so to get the face count down you can use the decimator module in Blender.

You also need to supplie the starting coordinates for the form, which can be found in the folder that was created when you collected the data.

But other than that, you are free to upload all the forms you want.

### Contributing
The Wi-Form project strive to evolve as people interact with it. So pull requests and forks are more than welcome. Rewrite, transform or remake the script in any way you see fit.




