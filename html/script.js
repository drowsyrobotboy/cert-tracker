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
        var eDate = new Date(cert.expiry);
        var rDays = Math.floor((eDate.getTime() - new Date().getTime())/86400000);
        var risk = "";
        if(rDays >= 15){
          risk = "✅ Expires in " + rDays + " days";
        } else if(rDays >= 7){
          risk = "⚠ Expires in " + rDays + " days";
        } else if (rDays > 0){
          risk = "🚨 Expires in " + rDays + " days";
        } else {
          risk = "☠️ Expired " + Math.abs(rDays) + " days ago";
        }
        tr.innerHTML = '<td>' + cert.hostname + '</td>' +
        '<td>' + cert.port + '</td>' +
        '<td>' + eDate.getDate() + "-" + eDate.getMonth()+1 + "-" + eDate.getFullYear() + '</td>' +
        '<td>' + risk + '</td>';
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