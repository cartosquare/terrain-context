## osm tags
This part of the program will extract osm tags from osm pbf data

### workflow
* Download a pbf format data from osm site of your study area
* Modify all_tags.csv to decide which tags you need and which not, this may depend on your study area
* use *filt_tags.py* to generate your interested tags to a file called *tags.csv*
* use *extract_pbf.py* to extract data of each tag to corresponding folder
* use *extract_download_list.py* to extract coordinate pairs of each tag
