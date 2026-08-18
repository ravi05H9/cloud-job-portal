import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Job, Application


def guess_category(title, skills):
    t = title.lower()
    if any(k in t for k in ["designer", "design intern", "ux designer", "ui/ux"]):
        return "Design"
    if any(k in t for k in ["developer", "engineer", "architect", "devops", "qa", "test engineer"]):
        return "Engineering"
    if any(k in t for k in ["data analyst", "data entry", "sql developer"]):
        return "Data"
    if any(k in t for k in ["marketing", "content writer", "content reviewer"]):
        return "Marketing"
    if any(k in t for k in ["sales", "customer", "support associate", "hr executive", "operations executive", "financial analyst"]):
        return "Customer Success"
    s = skills.lower()
    if any(k in s for k in ["figma", "adobe xd", "photoshop", "illustrator"]):
        return "Design"
    if any(k in s for k in ["sql", "power bi", "looker", "excel"]):
        return "Data"
    return "Engineering"


def guess_level(title):
    text = title.lower()
    if any(k in text for k in ["senior", "sr.", "lead"]):
        return "Senior"
    if any(k in text for k in ["intern", "entry", "associate", "junior"]):
        return "Entry"
    return "Mid"


def guess_type(title):
    text = title.lower()
    if "intern" in text:
        return "Internship"
    if "contract" in text:
        return "Contract"
    if "part-time" in text:
        return "Part-time"
    return "Full-time"


def job_list(request):
    jobs = Job.objects.all().order_by('-id')
    jobs_data = []
    for j in jobs:
        initials = "".join([w[0] for w in j.company.split()[:2]]).upper()
        tags = [s.strip() for s in j.skills.split(",")] if j.skills else []
        jobs_data.append({
            "id": j.id,
            "title": j.title,
            "company": j.company,
            "initials": initials,
            "color": "#E8A33D",
            "location": j.location,
            "type": guess_type(j.title),
            "category": guess_category(j.title, j.skills),
            "level": guess_level(j.title),
            "salary": j.salary,
            "posted": "Recently",
            "tags": tags,
            "blurb": j.description[:150],
        })
    return render(request, 'jobs/job_list.html', {
        'jobs': jobs,
        'jobs_json': jobs_data,
    })


def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    initials = "".join([w[0] for w in job.company.split()[:2]]).upper()
    tags = [s.strip() for s in job.skills.split(",")] if job.skills else []
    job_data = {
        "id": job.id,
        "title": job.title,
        "company": job.company,
        "initials": initials,
        "color": "#E8A33D",
        "location": job.location,
        "type": guess_type(job.title),
        "category": guess_category(job.title, job.skills),
        "level": guess_level(job.title),
        "salary": job.salary,
        "posted": "Recently",
        "tags": tags,
        "blurb": job.description,
    }
    return render(request, 'jobs/job_detail.html', {'job': job, 'job_json': job_data})


@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    already_applied = Application.objects.filter(job=job, applicant=request.user).exists()

    if request.method == "POST":
        if already_applied:
            messages.warning(request, "You have already applied to this job.")
            return redirect('my_applications')

        resume = request.FILES.get('resume')
        cover_letter = request.POST.get('cover_letter', '')

        if not resume:
            messages.error(request, "Please attach a resume (PDF, DOC, or DOCX).")
            return render(request, 'jobs/apply.html', {'job': job, 'already_applied': already_applied})

        application = Application(
            job=job,
            applicant=request.user,
            resume=resume,
            cover_letter=cover_letter,
        )
        try:
            application.full_clean()
            application.save()
        except ValidationError as e:
            error_msg = "; ".join([str(m) for m in e.messages])
            messages.error(request, f"Could not submit application: {error_msg}")
            return render(request, 'jobs/apply.html', {'job': job, 'already_applied': already_applied})

        messages.success(request, "Application submitted successfully!")
        return redirect('my_applications')

    return render(request, 'jobs/apply.html', {'job': job, 'already_applied': already_applied})


@login_required
def my_applications(request):
    applications = Application.objects.filter(
        applicant=request.user
    ).select_related('job').order_by('-applied_at')
    return render(request, 'accounts/my_applications.html', {'applications': applications})
