# core/forms.py
from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        # ดึงทุกฟิลด์ที่ออกแบบไว้ใน models.py
        fields = [
            'title', 'category', 'main_image', 'description', 

        ]
        # ใส่ Class Bootstrap ให้สวยงาม
        widgets = {
            field: forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'})
            for field in ['title', 'area',]
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ปรับแต่งเพิ่มเติมสำหรับ Textarea
        self.fields['description'].widget = forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 4})
        self.fields['category'].widget.attrs.update({'class': 'form-select bg-dark text-white border-secondary'})
        self.fields['year'].widget.attrs.update({'class': 'form-control bg-dark text-white border-secondary'})
        