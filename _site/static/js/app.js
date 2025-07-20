document.addEventListener('DOMContentLoaded', () => {
    // Cursor follower effect
    const cursorFollower = document.querySelector('.cursor-follower');
    document.addEventListener('mousemove', (e) => {
        gsap.to(cursorFollower, {
            x: e.clientX,
            y: e.clientY,
            duration: 0.025,
            ease: 'power1.out'
        });
    });

    // Fetch data from YAML file
    async function fetchPortfolioData() {
        try {
            const response = await fetch('/portfolio.yaml');
            const yamlText = await response.text();
            return jsyaml.load(yamlText);
        } catch (error) {
            console.error('Error fetching portfolio data:', error);
            return null;
        }
    }

    // Render about text
    function renderAboutText(aboutText) {
        const aboutTextContainer = document.getElementById('about-text');
        aboutTextContainer.innerHTML = `<p>${aboutText}</p>`;
    }

    // Render projects
    function renderProjects(projects) {
        const projectsContainer = document.getElementById('projects-container');
        projectsContainer.innerHTML = projects.map(project => `
            <div class="project-card">
                <h3>${project.title}</h3>
                <p>${project.description}</p>
                <div class="project-technologies">
                    <i data-feather="${project.icon}" class="mr-2"></i>
                    <span>Technologies: ${project.technologies.join(', ')}</span>
                </div>
            </div>
        `).join('');
    }

    // Render skills
    function renderSkills(skills) {
        const skillsContainer = document.getElementById('skills-container');
        skillsContainer.innerHTML = Object.entries(skills).map(([category, skillList]) => `
            <div class="skills-category">
                <h3>${category}</h3>
                <ul>
                    ${skillList.map(skill => `<li>${skill}</li>`).join('')}
                </ul>
            </div>
        `).join('');
    }

    // Render social links
    function renderSocialLinks(social) {
        const socialLinksContainer = document.getElementById('social-links');
        socialLinksContainer.innerHTML = social.map(link => `
            <a href="${link.url}" target="_blank" aria-label="${link.platform}">
                <i data-feather="${link.icon}" class="w-6 h-6"></i>
            </a>
        `).join('');
    }

    // Update page content
    function updatePageContent(data) {
        // Update header
        document.getElementById('name').textContent = data.name;
        document.getElementById('tagline').textContent = data.tagline;
        document.getElementById('page-title').textContent = `${data.name} - Portfolio`;
        document.getElementById('copyright').textContent = data.copyright;

        // Update professional image
        const professionalImage = document.getElementById('professional-image');
        if (data.professionalImage) {
            professionalImage.src = data.professionalImage;
            professionalImage.alt = `${data.name} Professional Photo`;
        }

        // Update about section
        renderAboutText(data.aboutText);

        // Render sections
        renderProjects(data.projects);
        renderSkills(data.skills);
        renderSocialLinks(data.social);
    }

    // Handle contact form submission
    function setupContactForm() {
        const contactForm = document.getElementById('contact-form');
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            // In a real-world scenario, you'd send this to a backend service
            const formData = new FormData(contactForm);
            const formObject = Object.fromEntries(formData.entries());

            try {
                // Simulate form submission
                console.log('Form submitted:', formObject);
                alert('Thank you for your message! I will get back to you soon.');
                contactForm.reset();
            } catch (error) {
                console.error('Error submitting form:', error);
                alert('There was an error sending your message. Please try again.');
            }
        });
    }

    // Initialize page
    async function initPage() {
        const data = await fetchPortfolioData();
        if (data) {
            updatePageContent(data);
        }

        // Replace feather icons after content is loaded
        feather.replace();

        // Setup contact form
        setupContactForm();
    }

    // Smooth scrolling for nav links
    function setupSmoothScrolling() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();

                const targetId = this.getAttribute('href');
                const targetElement = document.querySelector(targetId);

                if (targetElement) {
                    gsap.to(window, {
                        duration: 1,
                        scrollTo: {
                            y: targetElement,
                            offsetY: 80
                        },
                        ease: 'power3.inOut'
                    });
                }
            });
        });
    }

    // Load additional libraries for smooth scrolling
    function loadAdditionalLibraries() {
        return new Promise((resolve) => {
            const scrollToPlugin = document.createElement('script');
            scrollToPlugin.src = 'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.11.4/ScrollToPlugin.min.js';
            scrollToPlugin.onload = resolve;
            document.head.appendChild(scrollToPlugin);
        });
    }

    // Initialize everything
    Promise.all([
        new Promise(resolve => window.addEventListener('DOMContentLoaded', resolve)),
        loadAdditionalLibraries()
    ]).then(() => {
        initPage();
        setupSmoothScrolling();
    });
});