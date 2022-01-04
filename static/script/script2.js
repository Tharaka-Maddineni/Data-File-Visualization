// getting dataset and column 
var main = document.getElementById('tablename');
var sub1 = document.getElementById('col1');
var sub2 = document.getElementById('col2');

var columns_records_data = {};

// column data variables to plot
var plot_data = [];


// Trigger the event with dataset and columns
if (main != null)
{
  main.addEventListener('change', function(){    
    // // fetch columns and 25 records of each column from database by API to flask
    let id = this.value;
    let val = this.options[this.selectedIndex].text;

    const url = `/dataset/:${id}/plot`;

    fetch(url)
    .then(jsonData => jsonData.json())
    .then(data => datasets(data))

  // -----------------------------------------------------
    let datasets = (data) =>
    {
    // getting a selected option  
    var selected_option = data[val];

    Object.assign(columns_records_data, selected_option)
  
    // removing the sub menu options using while loop
    while (sub1.options.length > 0)
    {
      sub1.options.remove(0);
    }

    // Convert the selected object into array and create a options for each array elements
    // using Option constructor, it will create html element with the given value and innerText
  
    Array.from(Object.keys(selected_option))
    .forEach(function(el)
    {
      let option = new Option(el, el);  

      // append the child option in sub menu
      sub1.appendChild(option);
  
    });

    while (sub2.options.length > 0)
    {
      sub2.options.remove(0);
    }

    // Convert the selected object into array and create a options for each array elements
    // using Option constructor, it will create html element with the given value and innerText
  
    Array.from(Object.keys(selected_option))
    .forEach(function(el)
    {
      let option = new Option(el, el);  
      // append the child option in sub menu
      sub2.appendChild(option);
    });
    }
  });
}

document.getElementById('myPlotForm').addEventListener('submit', function(e)
{
  e.preventDefault()
  const column1 = document.getElementById('col1').value;
  const column2 = document.getElementById('col2').value;

  const data1 = {};
  
  for(const [key,value] of Object.entries(columns_records_data))
  {
    if (key === column1)
    {
      data1['x'] = value
    }
    else if (key == column2)
    {
      data1['y'] = value
    }
  }
  plot_data.push(data1)

  var layout = 
  {
    title: { text: 'Task Plot', font: { family: 'Courier New, monospace', size: 24 }, xref: 'paper', x: 0.05,},
    xaxis: {
      title: { text: column1, font: { family: 'Courier New, monospace', size: 18, color: '#7f7f7f'} },},
    yaxis: {
      title: { text: column2, font: { family: 'Courier New, monospace', size: 18, color: '#7f7f7f' } } }
  };
  var config = {responsive : true};
  Tester = document.getElementById('myPlot');

  Plotly.newPlot(Tester, plot_data, layout, config);
});