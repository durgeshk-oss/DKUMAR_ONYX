"""
DKumar ONYX v3.0 — Enterprise Risk Knowledge Graph
Generates interactive, transparent corporate network topologies mapping CVEs directly to frameworks with explicit group clustering.
"""
import plotly.graph_objects as go
try:
    import networkx as nx
    NX_AVAILABLE = True
except ImportError:
    NX_AVAILABLE = False

class RiskKnowledgeGraph:
    BUSINESS_UNITS = ["Infrastructure", "AppDev", "Data Platform", "Corporate IT", "Cloud Ops"]
    FRAMEWORKS     = ["NIST CSF", "ISO 27001", "SOX", "GDPR", "PIPEDA"]
    TECH_BU_MAP    = {"Linux": "Infrastructure", "Windows": "Infrastructure", "Apache": "AppDev", "Tomcat": "AppDev", "MySQL": "Data Platform", "General": "Corporate IT"}
    TYPE_COLORS    = {"framework": "#00d4ff", "business_unit": "#ffaa00", "cve": "#ff2055", "tech": "#00e87a"}

    def __init__(self):
        self.G = nx.Graph() if NX_AVAILABLE else None

    def build_from_risks(self, risks):
        if not NX_AVAILABLE or not risks: return
        self.G.clear()
        
        # Enforce structural clustering by injecting hierarchy weights into the network map
        for r in risks[:12]:
            cve = r.get('event', 'Unknown')
            tech = r.get('tech', 'General')
            bu = self.TECH_BU_MAP.get(tech, "Corporate IT")
            
            self.G.add_node(cve, type="cve", label=cve)
            self.G.add_node(tech, type="tech", label=tech)
            self.G.add_node(bu, type="business_unit", label=bu)
            
            # High stiffness (weight=3): Keeps the CVE locked close to its specific platform tech
            self.G.add_edge(cve, tech, weight=3)
            # Medium stiffness (weight=2): Anchors the tech to its organizational department
            self.G.add_edge(tech, bu, weight=2)
            
            for fw in self.FRAMEWORKS:
                self.G.add_node(fw, type="framework", label=fw)
                # Low stiffness (weight=1): Allows regulatory overlays to stretch outwards uniformly
                self.G.add_edge(bu, fw, weight=1)

    def render(self):
        if not NX_AVAILABLE or not self.G or len(self.G.nodes) == 0: return self._empty_figure()
        
        # k: Optimal distance between nodes. iterations: Higher values settle the cluster positioning.
        pos = nx.spring_layout(self.G, k=0.38, iterations=75, seed=42, weight='weight')
        
        edge_x, edge_y = [], []
        for edge in self.G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        node_x, node_y, node_colors, node_text = [], [], [], []
        for node in self.G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            n_type = self.G.nodes[node].get('type', 'tech')
            node_colors.append(self.TYPE_COLORS.get(n_type, "#ffffff"))
            node_text.append(self.G.nodes[node].get('label', ''))

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode='lines', line=dict(color='rgba(0,212,255,0.08)', width=1), hoverinfo='none'))
        fig.add_trace(go.Scatter(x=node_x, y=node_y, mode='markers+text', marker=dict(size=13, color=node_colors, line=dict(color='#04060a', width=1.5)), text=node_text, textposition='top center', textfont=dict(color='#e8f4ff', size=10, family='JetBrains Mono'), hovertemplate='<b>%{text}</b><extra></extra>'))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False, height=450, margin=dict(l=10,r=10,t=10,b=10), xaxis=dict(showgrid=False, zeroline=False, showticklabels=False), yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
        return fig

    def _empty_figure(self):
        fig = go.Figure()
        fig.add_annotation(text="Ingest operational logs or execute analytical passes to generate data clusters.", x=0.5, y=0.5, showarrow=False, font=dict(color='#5a7a99', size=12, family='JetBrains Mono'))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(visible=False), yaxis=dict(visible=False))
        return fig