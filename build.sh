set -o errexit

# Install dependencies
pip install -r requirements.txt

# Build the project
python manage.py collectstatic --noinput
python manage.py migrate