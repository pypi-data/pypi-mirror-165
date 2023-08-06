global DROPDOWN_COUNTER
DROPDOWN_COUNTER=0

def style_css_and_js():
    return '''<style>

tr:nth-child(even){background-color: #f2f2f2;}

td {
    padding:10px;
    border: 1px solid grey;
}

.dropbtn {
  background-color: grey;
  color: white;
  padding: 5px;
  border: none;
  cursor: pointer;
}

.dropbtn:hover, .dropbtn:focus {
  background-color: #2980B9;
}

.dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-content {
  display: none;
  position: absolute;
  padding:10px;
  background-color: #f1f1f1;
  min-width: 900px;
  overflow: auto;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
}

.show {display: block;}
</style>
</head>
<body>

<script>
function show_log(c) {
  document.getElementById("myDropdown" + String(c)).classList.toggle("show");
}
</script>'''

def dropdown_link(log):
    global DROPDOWN_COUNTER
    DROPDOWN_COUNTER = DROPDOWN_COUNTER + 1
    return '''<div class="dropdown">
  <button onclick="show_log(''' + str(DROPDOWN_COUNTER) + ''')" class="dropbtn">Log Content</button>
  <div id="myDropdown''' + str(DROPDOWN_COUNTER) + '''" class="dropdown-content">''' + log + '''
  </div>
</div>'''

class ReportHtml(object):
    def __init__(self):
        self.html = '<!doctype html><html><head><title>System Test Results</title>' + style_css_and_js() + '</head><body><table>'
        self.html = self.html + "<tr><td><b>Testcase</b></td><td><b>Log</b></td><td><b>Result</b></td><td><b>Testcase Duration (s)</b></td>"
        self.html = self.html + "<td><b>Retries(allowed)</b></td></tr>"

    def add_result(self, description, log, result, duration, retries):
        duration = '{:.5f}'.format(duration)
        color = "red"
        txt = "FAIL"
        if result:
            color = "green"
            txt = "PASS"

        log_html = ""
        if log.strip() != "":
            log_html = dropdown_link(log.replace("\n", "</br>"))
        self.html = self.html + '<tr>'
        self.html = self.html + '<td>' + description + '</td>'
        self.html = self.html + '<td>' + log_html + '</td>'
        self.html = self.html + '<td style="text-align:center;color:white;background-color:' + color + '">' + txt + '</td>'
        self.html = self.html + '<td style="text-align:center">' + str(duration) + '</td>'
        self.html = self.html + '<td style="text-align:center">' + str(retries[0]) + '(' + str(retries[1]) + ')</td>'
        self.html = self.html + "</tr>"

    def finish_results(self, output_file):
        self.html = self.html + "</table></body></html>"
        open(output_file, "w").write(self.html)