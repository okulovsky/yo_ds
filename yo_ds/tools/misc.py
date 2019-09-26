
from IPython.display import HTML

def notebook_printable_version(finalize):
    if finalize:
        return HTML('''<script>
        code_show=true; 
        function code_toggle() {
         if (code_show){
         $('div.input').hide();
         $("div[class='prompt output_prompt']").css('visibility','hidden');

         } else {
         $('div.input').show();
         $("div[class='prompt output_prompt']").css('visibility','visible');
         }
         code_show = !code_show
        } 
        $( document ).ready(code_toggle);
        </script>
        <a href="javascript:code_toggle()">Automatically generated report</a>.''')
    else:
        return None

import pandas as pd

def diffset(set1, set2, name1='First',name2='Second'):
    set1=set(set1)
    set2=set(set2)
    return pd.Series([
    len(set1),
    len(set2),
    len(set1-set2),
    len(set2-set1),
    len(set1.intersection(set2)),
    set1==set2,
    set1.issubset(set2),
    set2.issubset(set1),
    ],index=[name1,name2,'{0}-{1}'.format(name1,name2),'{0}-{1}'.format(name2,name1),"Intersection","Match",'LeftIsSubset','RightIsSubset']
)
