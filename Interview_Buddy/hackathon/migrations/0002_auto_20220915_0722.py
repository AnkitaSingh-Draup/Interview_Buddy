# Generated by Django 3.2 on 2022-09-15 07:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hackathon', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('mobile_number', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('core_skills', models.TextField()),
                ('soft_skills', models.TextField()),
                ('past_company', models.TextField()),
                ('years_of_exp', models.TextField(default=0)),
                ('past_title', models.TextField()),
            ],
            options={
                'unique_together': {('name', 'email')},
            },
        ),
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.TextField()),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hackathon.candidate')),
            ],
        ),
        migrations.CreateModel(
            name='Interviewer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp_id', models.IntegerField(unique=True)),
                ('name', models.TextField()),
                ('max_level', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_id', models.ImageField(unique=True, upload_to='')),
                ('job_type', models.TextField()),
                ('skills', models.TextField()),
                ('location', models.TextField()),
                ('description', models.TextField()),
                ('title', models.TextField()),
                ('core_skills', models.TextField()),
                ('soft_skills', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(unique=True)),
                ('tags', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='QuestionLevelRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hackathon.candidate')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hackathon.level')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hackathon.question')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('values', models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transcript',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vtt_file', models.TextField(unique=True)),
            ],
        ),
        migrations.DeleteModel(
            name='JobRole',
        ),
        migrations.AddField(
            model_name='questionlevelrating',
            name='rating',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hackathon.rating'),
        ),
        migrations.AddField(
            model_name='interview',
            name='interviewer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hackathon.interviewer'),
        ),
        migrations.AddField(
            model_name='interview',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hackathon.job'),
        ),
        migrations.AddField(
            model_name='interview',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hackathon.level'),
        ),
        migrations.AlterUniqueTogether(
            name='questionlevelrating',
            unique_together={('candidate', 'question', 'level', 'rating')},
        ),
        migrations.AlterUniqueTogether(
            name='interview',
            unique_together={('candidate', 'job', 'interviewer', 'level', 'result')},
        ),
    ]
