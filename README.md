# vppapihello
The Hello World of VPP API

# The link to the wiki description

https://wiki.fd.io/view/VPP/Python_API


# install preresquisites
sudo apt-get install python-virtualenv
 
export VPP=~vpp/
cd $VPP
 
# build vpp
make bootstrap build
 
# create virtualenv
virtualenv virtualenv
 
# (optional) install python packages
# ipaddress is used by some scripts
virtualenv/bin/pip install ipaddress
# nice to have to get the tab completion and other CLI niceties
virtualenv/bin/pip install scapy
 
# install vpp python api
pushd $VPP/src/vpp-api/python/
$VPP/virtualenv/bin/python setup.py install
popd
 
# Now set the LD_LIBRARY_PATH such that it points to the directory containing libvppapiclient.so
export LD_LIBRARY_PATH=`find $VPP -name "libvppapiclient.so" -exec dirname {} \; | grep install-vpp | head -n 1`
 
# You will now need two windows :
# one for vpp, and the other for python
 
# VPP
cd $VPP
make run
 
# python
# (as root, as vpp.connect() requires root privileges)
# Note that sudo cannot not preserve LD_LIBRARY_PATH
cd $VPP
 
# you can run a script 
sudo -E LD_LIBRARY_PATH=$LD_LIBRARY_PATH $VPP/virtualenv/bin/python vpp-api/python/tests/vpp_hello_world.py.py
 
# or get a python prompt
sudo -E LD_LIBRARY_PATH=$LD_LIBRARY_PATH $VPP/virtualenv/bin/python
VPP python'