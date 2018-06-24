# Script to export templates and static files from app
echo "Coping templates files to deploy";
cp -r Inventory/templates/ deploy/app/templates

echo "Sort files on deploy/templates";
mv deploy/app/templates/templates/* deploy/app/templates
rm -r deploy/app/templates/templates/

echo "Sucessfully, next coping static files to deploy";
cp -r Inventory/static/ deploy/app/files

echo "Sort files on deploy/app/static";
mv deploy/app/files/static/* deploy/app/files
rm -r deploy/app/files/static

echo "Move database";
cp Inventory/database/DB.db deploy/app/files
