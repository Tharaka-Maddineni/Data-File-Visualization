// getting dataset and column 
var main = document.getElementById('datasets');
var sub = document.getElementById('columns');

// Trigger the event with dataset and columns
if (main != null)
{
   main.addEventListener('change', function(){    
    // // fetch columns from database by API to flask
    let id = this.value;
    let val = this.options[this.selectedIndex].text;

    /////// Get request to fetch table columns from given table name ////////
    const url = `/dataset/:${id}/compute`; 

    fetch(url)
    .then(jsonData => jsonData.json())
    .then(data => datasets(data))

    let datasets = (data) =>
    {
    // getting a selected option  
    var selected_option = data[val];

    // removing the sub menu options using while loop
    while (sub.options.length > 0)
    {
      sub.options.remove(0);
    }

    // Convert the selected object into array and create a options for each array elements
    // using Option constructor, it will create html element with the given value and innerText
  
    Array.from(selected_option)
    .forEach(function(el)
    {
      let option = new Option(el, el);
  
      // append the child option in sub menu
      sub.appendChild(option);
    });
    }
  });
}

//---------------------------------------------------------------
const myForm = document.getElementById('myForm');

myForm.addEventListener('submit', function (e){
  e.preventDefault();


  const formData = new FormData(this);
  const searchParams = new URLSearchParams();


  let main = document.getElementById('datasets');
  let id  = main.options[main.selectedIndex].value;
  
  const url = `/dataset/:${id}/compute`; 

  // for( var x of formData)
  // {
  //   console.log(x)
  // }

  fetch(url, { method : 'post', body : formData})
  .then(function (response)
  {
    return response.json();
  })
  .then(function (json)
  {
    result_value = json['result_value'];
    console.log(result_value);
    document.getElementById('compute_output').textContent = result_value;
  })
  .catch(err => console.log(err))

});