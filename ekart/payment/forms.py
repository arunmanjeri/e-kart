from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields=['first_name','last_name','phone','email','address_line_1','address_line_2','country','state','city','order_note']
    def __init__(self,*args,**kwargs): 
        super(OrderForm,self).__init__(*args,**kwargs)
        self.fields['order_note']=forms.CharField(widget=forms.Textarea)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
        
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
