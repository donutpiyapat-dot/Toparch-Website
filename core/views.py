from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Case, When, IntegerField, Value,F
from django.http import Http404
from django.core.paginator import Paginator
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank,TrigramSimilarity
from .models import Project, Document, Category
from django.db.models.functions import Greatest



def home_view(request):
    return render(request, 'index.html')

def services_view(request):
    return render(request, 'services.html')

def ta_style(request):
    return render(request, 'ta_style.html')

def infocus_view(request):
    return render(request, 'infocus.html')

def contact(request):
    return render(request, 'contact.html')

def projects(request):
    query = request.GET.get('q')
    category = request.GET.get('cat')
    
    projects = Project.published.select_related('category').order_by('-created_at')

    selected_category = None
    if category and category.lower() != 'all':
        selected_category = Category.objects.filter(slug=category).first()
        projects = projects.filter(category__slug=category)

    if query:
        projects = projects.filter(
            Q(title__icontains=query) |
            Q(category__name__icontains=query)
        )

    categories = Category.objects.all()

    paginator = Paginator(projects, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    total_projects = projects.count()
    total_categories = Category.objects.count()

    return render(request, 'projects.html', {
        'page_obj': page_obj,
        'query': query,
        'current_cat': category or 'All',
        'total_projects': total_projects,
        'total_categories': total_categories,
        'categories': categories,
        'selected_category': selected_category,
    })


def projects_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)

    images = project.images.all() 

    images_set1 = project.images.filter(image_type='set1')
    images_set2 = project.images.filter(image_type='set2')

    next_project = Project.published.filter(id__gt=project.id).order_by('id').first()
    previous_project = Project.published.filter(id__lt=project.id).order_by('-id').first()

    return render(request, 'projects_detail.html', {
        'project': project,
        'images': images,
        'images_set1': images_set1,
        'images_set2': images_set2,
        'next_project': next_project,
        'previous_project': previous_project,
    })

def services_detail(request, slug):
    services = {
        "services-1": {
            "title": "DESIGN PERIOD",
            "description": "During this phase, our architects and engineers analyze the client’s requirements, study site conditions and regulations, and develop design concepts that align with functionality, budget, and environmental context. We prepare complete architectural drawings, structural engineering designs, building systems engineering (MEP), and all necessary design documentation.",
        },
        "services-2": {
            "title": "PRE-CONSTRUCTION PERIOD",
            "description": "This phase focuses on preparing all necessary aspects before construction begins, including cost estimation, budget planning, preparation of tender documents, contractor selection, and project planning to ensure that the construction process runs efficiently.",
        },
        "services-3": {
            "title": "Construction Period",
            "description": "During construction, our team supervises, inspects, and manages the construction work to ensure it complies with the design, engineering standards, and project timeline. We also coordinate closely between the project owner, contractors, and all related parties.",
        },
        "services-4": {
            "title": "Post-Construction Period",
            "description": "Once construction is completed, we conduct quality inspections, project acceptance procedures, and prepare project handover documentation to ensure that the building or development is ready for operation and meets all required standards.",
        },
        "services-5": {
            "title": "After Construction Period",
            "description1": "After project handover, we provide post-construction support including operational follow-up, inspections during the warranty period, and maintenance recommendations to ensure the long-term performance of building systems and components.",
            "description2": "We also provide building survey and measurement services for existing structures, including assessment of structural systems, electrical systems, and building services, to support redesign, renovation, or building improvement projects.",
        },
    }

    if slug not in services:
        raise Http404("Service not found")

    return render(request, "services_detail.html", {
        "service": services[slug] 
    })

def global_search(request):
    query = request.GET.get('q')
    results = Project.published.all()

    if query:

        search_vector = (
            SearchVector('title', weight='A') +
            SearchVector('category__name', weight='B') +
            SearchVector('area', weight='C') +
            SearchVector('description', weight='D')
        )

        search_query = SearchQuery(query, search_type='websearch')

        results = results.annotate(
            rank=SearchRank(search_vector, search_query),

            trigram=(
                TrigramSimilarity('title', query) +
                TrigramSimilarity('category__name', query) +
                TrigramSimilarity('area', query)
            )
        ).annotate(
            score=F('rank') + F('trigram')

        ).filter(
            score__gt=0.1
        ).order_by('-score')

    return render(request, 'search_results.html', {
        'projects': results,
        'query': query,
        'total_results': results.count()
    })



@login_required
def document_list(request):
    query = request.GET.get('q')

    documents = Document.objects.all()

    if query:
        documents = documents.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    documents = documents.order_by('-uploaded_at')

    return render(request, 'document_list.html', {
        'documents': documents,
        'query': query
    })


import random

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    images = list(project.images.all())

    prev_big = False  

    for img in images:
        img.size = random.choices(
            ['small', 'medium', 'big'],
            weights=[5, 3, 2]
        )[0]

        if img.size == 'big':
            if prev_big or random.random() < 0.4:
                img.size = 'medium'
                prev_big = False
            else:
                prev_big = True
        else:
            prev_big = False

    return render(request, 'project_detail.html', {
        'project': project,
        'images': images
    })