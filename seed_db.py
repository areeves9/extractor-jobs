import csv
import os

from jobs.models import Job # imports the model
with open('jobs_2020.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        job = Job(
            description=row['Description'], 
            expiration_date=row['Expiration Date'],
            employment_type=row['Employment Type'],
            education=row['Education'],
            headline=row['Headline'],
            post_date=row['Post Date'],
            slug=row['Slug'],
            location=row['Location'],
            salary=row['Salary'],
            salary_frequency=row['Salary Frequency'],
            benefits=row['Benefits'],
            link=row['Link'],
            job_title=row['Job Title'],
        )
        job.save()