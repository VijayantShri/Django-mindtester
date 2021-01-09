window.onload = initall;
var saveAnsButton ;
function initall() {
	saveAnsButton = document.getElementById('save_ans')
	saveAnsButton.onclick = saveAns
}
function saveAns() {
	var ans = $("input:radio[name=radio]:checked").val()
	alert("Answer is submitted...")
	var req = new XMLHttpRequest();
	var url = "/saveAns?ans="+ans 
	req.open("GET", url, true)
	req.send()
}