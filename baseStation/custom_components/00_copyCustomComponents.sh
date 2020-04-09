# Check that the custom_components folder exists in the homeassistant config folder
mkdir -p /home/pi/homeassistant/custom_components;
# Copy the feedparser
cd feedparser-master/custom_components
cp -r feedparser /home/pi/homeassistant/custom_components/