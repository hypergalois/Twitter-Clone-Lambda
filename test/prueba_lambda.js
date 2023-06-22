const data = {
    name: "John",
  };
  
  const options = {
    method: 'POST',
    body: JSON.stringify(data),
    headers: {
      'Content-Type': 'application/json'
    }
  };
  
  fetch('https://sjjf4wbfusl54cobt3sbkdwnsm0ukjsc.lambda-url.us-east-1.on.aws/', options)
    .then(response => response.json())
    .then(data => {
      console.log(data.body);
    })
    .catch(error => {
      console.error('Error:', error);
    });
  
