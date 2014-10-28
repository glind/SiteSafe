from django import forms
from codemirror import CodeMirrorTextarea

codemirror_widget = CodeMirrorTextarea(mode="python", theme="cobalt", config={'fixedGutter': True})
document = forms.TextField(widget=codemirror_widget)