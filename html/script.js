var url = 'pepper.json';

function expiryCompare( a, b ) {
    dateA = new Date (a.expiry);
    dateB = new Date (b.expiry);

    if ( dateA.getTime() < dateB.getTime()){
      return -1;
    }
    if ( dateA.getTime() > dateB.getTime()){
      return 1;
    }
    return 0;
  }

function printer(response){
    certs = JSON.parse(response).sort(expiryCompare);
    console.log(certs);
    var table = document.getElementById('ctable');
    certs.forEach(cert => {
        var tr = document.createElement('tr');
        tr.innerHTML = '<td>' + cert.hostname + '</td>' +
        '<td>' + cert.port + '</td>' +
        '<td>' + new Date (cert.expiry) + '</td>';
        table.appendChild(tr);
    });
}

function load(url, callback) {
    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            callback(xhr.response);
        }
    }
    xhr.open('GET', url, true);
    xhr.send('');
}

load(url, printer);