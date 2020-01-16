import csv
import os

from cities_light.models import City
from jobs.models import Job # imports the model

direc = os.path.dirname(os.path.abspath(__file__))

def create_job_instance(row):
    job = Job(
        description=row['description'], 
        expiration_date=row['expiration_date'],
        employment_type=row['employment_type'],
        education=row['education'],
        headline=row['headline'],
        post_date=row['post_date'],
        slug=row['slug'],
        location=row['location'],
        salary=row['salary'],
        salary_frequency=row['salary_frequency'],
        benefits=row['benefits'],
        link=row['link'],
        job_title=row['job_title'],
    )
    job.save()

with open('jobs_2020.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    with open(f'{direc}/jobs_20201.csv', 'w') as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                'description', 
                'expiration_date',
                'employment_type',
                'education',
                'headline',
                'post_date',
                'slug',
                'location',
                'salary',
                'salary_frequency',
                'benefits',
                'link',
                'job_title',
            ])
        writer.writeheader()
        for row in csv_reader:
            city_name = row['location']
            city = City.objects.get(name=city_name)
            row['location'] = city
            writer.writerow(row)
            create_job_instance(row)



    

    
        