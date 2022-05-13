from django.shortcuts import render,redirect
from . models import Task
from . form import TodoForms
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView,DeleteView
from django.urls import reverse_lazy
# Create your views here.
class TaskListView(ListView):
    model = Task
    template_name = 'task_view.html'
    context_object_name ='obj'
class TaskDetailView(DetailView):
    model=Task
    template_name = 'detail.html'
    context_object_name = 'i'

class TaskUpdateView(UpdateView):
    model=Task
    template_name ='update.html'
    context_object_name = 'task'
    fields = ('name','priority','date')
    def get_success_url(self):
        return reverse_lazy('detailview',kwargs={'pk':self.object.id})

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('listview')

def task_view(request):
    if request.method=='POST':
        name=request.POST.get('name')
        priority=request.POST.get('priority')
        date=request.POST.get('date')
        obj=Task(name=name,priority=priority,date=date)
        obj.save()
    objs=Task.objects.all()
    return render(request,'task_view.html',{'obj':objs})

def delete(request,taskid):
    obj=Task.objects.get(id=taskid)
    if request.method=='POST':
        obj.delete()
        return redirect('/')
    return render(request,'delete.html',{'obj':obj})

def update(request,id):
    obj=Task.objects.get(id=id)
    form=TodoForms(request.POST or None,instance=obj)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request,'edit.html',{'form':form,'obj':obj})

