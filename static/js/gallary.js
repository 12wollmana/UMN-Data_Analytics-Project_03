var wrapper_attribute = document.getElementById("attribute");

var myHTML_attribue = '';
var attributes = ['Acousticness_percent','Danceability_percent',
'Energy_percent','Liveness_percent','Loudness_percent',
'Speechiness_percent','Tempo_percent','Valence_percent'];


for (var i = 0; i < 8; i++) {
    myHTML_attribue += '<div class="card col-md-12"><h6><b>'+  attributes[i] +' count by cluster' +'</b></h6><img src="../static/images/plots/attributes/'+ attributes[i] + '.png" alt="Avatar" style="width:100%"><div class="container"></div></div>'
}
wrapper_attribute.innerHTML = myHTML_attribue



var wrapper_decades = document.getElementById("decades");

var myHTML_decades = '';
var decades = ['Number_of_hits','Number_ones','Acousticness',
'Speechiness','Key','Energy','Tempo','Loudness','Danceability',
'Placement','Valence','Liveness'];


for (var i = 0; i < 10; i++) {
    myHTML_decades += '<div class="card col-md-6"><h6><b>'+  decades[i]  +' through the decades</b></h6><img src="../static/images/plots/decades/line/'+ decades[i] + '.png" alt="Avatar" style="width:100%"><div class="container"></div></div>'
}
wrapper_decades.innerHTML = myHTML_decades

var myHTML_topsongs = '';
var topsongs = ['Scattersongs1-20','Scattersongs21-40','Scattersongs41-60',
'Scattersongs61-80','Scattersongs81-100','Songs1-20','Songs21-40',
'Songs41-60','Songs61-80','Songs81-100','Acousticness',
'Danceability','Energy','Hits-per-rank','Key',
'Liveness','Loudness','Tempo','Valence'];


for (var i = 0; i < 20; i++) {
    myHTML_topsongs += '<div class="card col-sd-6"><h6><b>'+  topsongs[i]  +'</b></h6><img src="../static/images/plots/attributes/'+ topsongs[i] + '.png" alt="Avatar" style="width:100%"><div class="container"></div></div>'
}
wrapper_topsongs.innerHTML = myHTML_topsongs;

