from jinja2 import Template
HTML_TEMPLATE = """
<h1>Network Scan Report</h1>
<p>Devices Found: {{ count }}</p>

{% for dev in devices %}
<hr>
<h3>{{ dev.ip }} ({{ dev.vendor }})</h3>
<b>MAC:</b> {{ dev.mac }}<br>
<b>OS Guess:</b> {{ dev.os }}<br>
<b>Open Ports:</b> {{ dev.open_ports }}<br>
<b>Issues:</b>
<ul>
    {% for issue in dev.issues %}
        <li>{{ issue }}</li>
    {% endfor %}
</ul>
{% endfor %}
"""

def generate_html_report(devices):
    template = Template(HTML_TEMPLATE)
    return template.render(count=len(devices), devices=devices)
