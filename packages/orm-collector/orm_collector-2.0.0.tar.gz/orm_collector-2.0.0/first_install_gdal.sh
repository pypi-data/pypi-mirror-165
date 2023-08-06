version=$(gdal-config --version)
echo $version
pip install GDAL==$version
