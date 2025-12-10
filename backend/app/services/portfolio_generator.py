from app.models import PortfolioData
from typing import Dict
import os
from pathlib import Path

class PortfolioGenerator:
    """
    Generates HTML/CSS/JS portfolio from structured data
    """
    
    def __init__(self):
        # Path to template files
        self.templates_dir = Path(__file__).parent.parent / "templates"
    
    def generate(self, data: PortfolioData, template: str = "template1") -> Dict[str, str]:
        """
        Main generation method
        
        Args:
            data: Structured portfolio data
            template: Template name (template1, template2, template3)
            
        Returns:
            Dictionary with html, css, and js content
        """
        
        if template == "template1":
            return self._generate_template1(data)
        elif template == "template2":
            return self._generate_template2(data)
        elif template == "template3":
            return self._generate_template3(data)
        else:
            raise ValueError(f"Unknown template: {template}")
    
    def _generate_template1(self, data: PortfolioData) -> Dict[str, str]:
        """
        Generate modern, minimal portfolio
        """
        
        # Build experience section HTML
        experience_html = ""
        for exp in data.experience:
            responsibilities = "".join([f"<li>{resp}</li>" for resp in exp.responsibilities])
            experience_html += f"""
            <div class="experience-item">
                <h3>{exp.position} at {exp.company}</h3>
                <p class="date">{exp.start_date} - {exp.end_date or 'Present'}</p>
                {f'<p class="description">{exp.description}</p>' if exp.description else ''}
                {f'<ul class="responsibilities">{responsibilities}</ul>' if exp.responsibilities else ''}
            </div>
            """
        
        # Build education section HTML
        education_html = ""
        for edu in data.education:
            education_html += f"""
            <div class="education-item">
                <h3>{edu.degree}{f' in {edu.field}' if edu.field else ''}</h3>
                <p class="institution">{edu.institution}</p>
                <p class="date">{edu.start_date} - {edu.end_date}</p>
                {f'<p class="gpa">GPA: {edu.gpa}</p>' if edu.gpa else ''}
            </div>
            """
        
        # Build skills section HTML
        skills_html = "".join([f'<span class="skill-tag">{skill}</span>' for skill in data.skills])
        
        # Build projects section HTML
        projects_html = ""
        for proj in data.projects:
            tech_tags = "".join([f'<span class="tech-tag">{tech}</span>' for tech in proj.technologies])
            projects_html += f"""
            <div class="project-card">
                <h3>{proj.name}</h3>
                <p>{proj.description}</p>
                <div class="tech-stack">{tech_tags}</div>
                <div class="project-links">
                    {f'<a href="{proj.link}" target="_blank">Live Demo</a>' if proj.link else ''}
                    {f'<a href="{proj.github}" target="_blank">GitHub</a>' if proj.github else ''}
                </div>
            </div>
            """
        
        # Complete HTML document
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data.personal_info.name} - Portfolio</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}

        /* Header Styles */
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 0;
            text-align: center;
        }}

        .header h1 {{
            font-size: 3rem;
            margin-bottom: 10px;
        }}

        .location {{
            font-size: 1.1rem;
            opacity: 0.9;
            margin-bottom: 20px;
        }}

        .contact-info {{
            margin: 20px 0;
        }}

        .contact-info a,
        .contact-info span {{
            color: white;
            text-decoration: none;
            margin: 0 15px;
            font-size: 1rem;
        }}

        .contact-info a:hover {{
            text-decoration: underline;
        }}

        .social-links {{
            margin-top: 20px;
        }}

        .social-links a {{
            color: white;
            text-decoration: none;
            margin: 0 10px;
            padding: 8px 20px;
            border: 2px solid white;
            border-radius: 25px;
            display: inline-block;
            transition: all 0.3s;
        }}

        .social-links a:hover {{
            background: white;
            color: #667eea;
        }}

        /* Section Styles */
        section {{
            background: white;
            margin: 40px 0;
            padding: 60px 0;
        }}

        section h2 {{
            font-size: 2.5rem;
            margin-bottom: 30px;
            color: #667eea;
            text-align: center;
        }}

        /* Summary Section */
        .summary p {{
            font-size: 1.2rem;
            text-align: center;
            max-width: 800px;
            margin: 0 auto;
            color: #666;
        }}

        /* Experience Section */
        .experience-item {{
            margin-bottom: 40px;
            padding: 20px;
            border-left: 4px solid #667eea;
            background: #f9f9f9;
        }}

        .experience-item h3 {{
            font-size: 1.5rem;
            color: #333;
            margin-bottom: 10px;
        }}

        .date {{
            color: #667eea;
            font-weight: 600;
            margin-bottom: 15px;
        }}

        .description {{
            margin-bottom: 15px;
            color: #666;
        }}

        .responsibilities {{
            list-style-position: inside;
            color: #666;
        }}

        .responsibilities li {{
            margin-bottom: 8px;
        }}

        /* Education Section */
        .education-item {{
            margin-bottom: 30px;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 8px;
        }}

        .education-item h3 {{
            font-size: 1.4rem;
            color: #333;
            margin-bottom: 8px;
        }}

        .institution {{
            font-size: 1.1rem;
            color: #667eea;
            font-weight: 600;
            margin-bottom: 5px;
        }}

        .gpa {{
            color: #666;
            margin-top: 5px;
        }}

        /* Skills Section */
        .skills-container {{
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 15px;
        }}

        .skill-tag {{
            background: #667eea;
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            font-size: 0.95rem;
            font-weight: 500;
        }}

        /* Projects Section */
        .projects-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-top: 30px;
        }}

        .project-card {{
            background: #f9f9f9;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }}

        .project-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }}

        .project-card h3 {{
            font-size: 1.3rem;
            color: #333;
            margin-bottom: 15px;
        }}

        .project-card p {{
            color: #666;
            margin-bottom: 20px;
        }}

        .tech-stack {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 20px;
        }}

        .tech-tag {{
            background: #e0e7ff;
            color: #667eea;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.85rem;
        }}

        .project-links a {{
            display: inline-block;
            margin-right: 15px;
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
        }}

        .project-links a:hover {{
            text-decoration: underline;
        }}

        /* Footer */
        footer {{
            background: #333;
            color: white;
            text-align: center;
            padding: 30px 0;
        }}

        /* Responsive Design */
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2rem;
            }}
            
            section h2 {{
                font-size: 2rem;
            }}
            
            .projects-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <!-- Header Section -->
    <header class="header">
        <div class="container">
            <h1>{data.personal_info.name}</h1>
            {f'<p class="location">{data.personal_info.location}</p>' if data.personal_info.location else ''}
            <div class="contact-info">
                {f'<a href="mailto:{data.personal_info.email}">{data.personal_info.email}</a>' if data.personal_info.email else ''}
                {f'<span>{data.personal_info.phone}</span>' if data.personal_info.phone else ''}
            </div>
            <div class="social-links">
                {f'<a href="{data.personal_info.linkedin}" target="_blank">LinkedIn</a>' if data.personal_info.linkedin else ''}
                {f'<a href="{data.personal_info.github}" target="_blank">GitHub</a>' if data.personal_info.github else ''}
                {f'<a href="{data.personal_info.website}" target="_blank">Website</a>' if data.personal_info.website else ''}
            </div>
        </div>
    </header>

    <!-- Summary Section -->
    {f'''<section class="summary">
        <div class="container">
            <h2>About Me</h2>
            <p>{data.summary}</p>
        </div>
    </section>''' if data.summary else ''}

    <!-- Experience Section -->
    {f'''<section class="experience">
        <div class="container">
            <h2>Experience</h2>
            {experience_html}
        </div>
    </section>''' if data.experience else ''}

    <!-- Education Section -->
    {f'''<section class="education">
        <div class="container">
            <h2>Education</h2>
            {education_html}
        </div>
    </section>''' if data.education else ''}

    <!-- Skills Section -->
    {f'''<section class="skills">
        <div class="container">
            <h2>Skills</h2>
            <div class="skills-container">
                {skills_html}
            </div>
        </div>
    </section>''' if data.skills else ''}

    <!-- Projects Section -->
    {f'''<section class="projects">
        <div class="container">
            <h2>Projects</h2>
            <div class="projects-grid">
                {projects_html}
            </div>
        </div>
    </section>''' if data.projects else ''}

    <!-- Footer -->
    <footer>
        <div class="container">
            <p>&copy; 2024 {data.personal_info.name}. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>"""

        return {
            "html": html,
            "css": "",  # CSS is embedded in HTML
            "js": ""
        }
    
    def _generate_template2(self, data: PortfolioData) -> Dict[str, str]:
        """
        Generate a different template style (you can customize this)
        """
        # For now, use template1
        return self._generate_template1(data)
    
    def _generate_template3(self, data: PortfolioData) -> Dict[str, str]:
        """
        Generate another template style (you can customize this)
        """
        # For now, use template1
        return self._generate_template1(data)