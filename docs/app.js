document.addEventListener('DOMContentLoaded', () => {
    // Terminal Animation
    const commands = [
        "devinstaller search python",
        "devinstaller install nodejs docker vscode",
        "devinstaller update --all",
        "devinstaller list --installed"
    ];
    let cmdIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    let typingDelay = 100;
    let deletingDelay = 50;
    let pauseEnd = 2000;
    let pauseStart = 500;

    const typingElement = document.getElementById('terminal-typing');

    function typeTerminal() {
        if (!typingElement) return;
        
        const currentCmd = commands[cmdIndex];
        
        if (isDeleting) {
            typingElement.textContent = currentCmd.substring(0, charIndex - 1);
            charIndex--;
        } else {
            typingElement.textContent = currentCmd.substring(0, charIndex + 1);
            charIndex++;
        }

        let typeSpeed = isDeleting ? deletingDelay : typingDelay;

        if (!isDeleting && charIndex === currentCmd.length) {
            typeSpeed = pauseEnd;
            isDeleting = true;
        } else if (isDeleting && charIndex === 0) {
            isDeleting = false;
            cmdIndex = (cmdIndex + 1) % commands.length;
            typeSpeed = pauseStart;
        }

        setTimeout(typeTerminal, typeSpeed);
    }
    
    setTimeout(typeTerminal, 1000);

    // OS Detection and Downloads
    const repo = 'faizanfatmi/DevInstaller';
    const apiUrl = `https://api.github.com/repos/${repo}/releases/latest`;
    
    const downloadBtn = document.getElementById('download-btn');
    const downloadLabel = document.getElementById('download-label');
    const downloadMeta = document.getElementById('download-meta');
    const osIcon = document.getElementById('download-os-icon');
    
    const otherBtn = document.getElementById('other-platforms-btn');
    const platformDropdown = document.getElementById('platform-dropdown');
    const dropdownInner = platformDropdown.querySelector('.platform-dropdown__inner');

    const icons = {
        windows: `<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M0 3.449L9.75 2.1v9.451H0m10.949-9.602L24 0v11.4H10.949M0 12.6h9.75v9.451L0 20.699M10.949 12.6H24V24l-12.9-1.801"/></svg>`,
        macos: `<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M18.715 15.228c-.035-3.155 2.585-4.697 2.705-4.774-1.464-2.146-3.738-2.438-4.549-2.476-1.928-.194-3.763 1.135-4.743 1.135-.975 0-2.493-1.109-4.084-1.079-2.046.031-3.931 1.189-4.978 3.007-2.122 3.676-.541 9.103 1.517 12.083 1.011 1.46 2.203 3.095 3.791 3.036 1.516-.062 2.085-.98 3.826-.98 1.74 0 2.26.98 3.847.95 1.626-.03 2.65-1.488 3.64-2.946 1.144-1.674 1.615-3.295 1.636-3.376-.036-.015-3.161-1.213-3.194-4.598h-.011zM15.42 6.818c.84-1.018 1.406-2.433 1.251-3.843-1.219.049-2.685.811-3.543 1.815-.762.883-1.442 2.327-1.263 3.714 1.365.105 2.713-.67 3.555-1.686z"/></svg>`,
        linux: `<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12.639 0c-3.149 0-4.015 1.758-4.015 1.758s.867 1.83 2.089 2.58c.95-.316 2.072-.257 2.072-.257s1.396-.135 1.666 1.077c-.943.468-1.58.125-1.58.125s-.834.793 1.724 1.332C12.64 8.1 11.2 8.441 11.2 8.441s-1.895-.885-3.374-.183c-.347-1.127-1.196-1.597-2.228-1.635-1.09-.041-2.186.425-2.617 1.503-.668 1.671.397 3.23 1.954 3.769 1.488.514 2.898-1.018 2.898-1.018s.709-.588 1.685.207c0 0-2.316 1.888-2.631 3.52-.315 1.632-.58 3.593 1.334 3.593 1.915 0 2.215-1.859 2.215-2.02v-1.42s1.474-1.353 3.056-1.353c1.583 0 2.457 1.353 2.457 1.353v1.419c0 .162.3 2.021 2.215 2.021 1.915 0 1.65-1.961 1.334-3.593-.315-1.632-2.63-3.52-2.63-3.52.975-.795 1.685-.207 1.685-.207s1.41 1.532 2.898 1.018c1.557-.539 2.622-2.098 1.954-3.769-.431-1.078-1.527-1.544-2.617-1.503-1.031.038-1.88.508-2.227 1.635-1.48-.702-3.375.183-3.375.183s-1.44-.341-3.395-1.826c2.558-.539 1.724-1.332 1.724-1.332s-.637.343-1.58-.125c.27-1.212 1.666-1.077 1.666-1.077s1.122-.059 2.072.257c1.222-.75 2.089-2.58 2.089-2.58S15.788 0 12.639 0zm-4.707 6.136c.642 0 1.162.52 1.162 1.162 0 .642-.52 1.162-1.162 1.162-.642 0-1.162-.52-1.162-1.162 0-.642.52-1.162 1.162-1.162zm9.414 0c.642 0 1.162.52 1.162 1.162 0 .642-.52 1.162-1.162 1.162-.642 0-1.162-.52-1.162-1.162 0-.642.52-1.162 1.162-1.162z"/></svg>`
    };

    function getOS() {
        const userAgent = window.navigator.userAgent.toLowerCase();
        const platform = window.navigator.platform.toLowerCase();
        
        if (platform.includes('win') || userAgent.includes('windows')) return 'windows';
        if (platform.includes('mac') || userAgent.includes('mac')) return 'macos';
        if (platform.includes('linux') || userAgent.includes('linux')) return 'linux';
        return 'windows'; // Default
    }

    const currentOS = getOS();

    // Fetch releases
    fetch(apiUrl)
        .then(res => res.json())
        .then(data => {
            const version = data.tag_name || 'Latest';
            const assets = data.assets || [];

            const downloads = {
                windows: assets.find(a => a.name.endsWith('.exe')),
                macos: assets.find(a => a.name.endsWith('.dmg')),
                linux: assets.find(a => a.name.endsWith('.AppImage'))
            };

            // Setup primary button
            const primaryAsset = downloads[currentOS];
            if (primaryAsset) {
                downloadBtn.disabled = false;
                downloadBtn.onclick = () => window.location.href = primaryAsset.browser_download_url;
                
                const osName = currentOS === 'macos' ? 'macOS' : currentOS.charAt(0).toUpperCase() + currentOS.slice(1);
                downloadLabel.textContent = `Download for ${osName}`;
                osIcon.innerHTML = icons[currentOS];
                
                const sizeMB = (primaryAsset.size / (1024 * 1024)).toFixed(1);
                downloadMeta.textContent = `${version} · ${sizeMB} MB`;
            } else {
                downloadLabel.textContent = 'Go to GitHub Releases';
                downloadMeta.textContent = 'See all downloads';
                downloadBtn.disabled = false;
                downloadBtn.onclick = () => window.open(data.html_url, '_blank');
            }

            // Populate dropdown
            dropdownInner.innerHTML = '';
            const allPlatforms = [
                { id: 'windows', name: 'Windows (.exe)' },
                { id: 'macos', name: 'macOS (.dmg)' },
                { id: 'linux', name: 'Linux (.AppImage)' }
            ];

            allPlatforms.forEach(p => {
                const asset = downloads[p.id];
                if (asset) {
                    const btn = document.createElement('a');
                    btn.href = asset.browser_download_url;
                    btn.className = 'platform-option';
                    
                    const sizeMB = (asset.size / (1024 * 1024)).toFixed(1);
                    
                    btn.innerHTML = `
                        <span class="platform-option__icon">${icons[p.id]}</span>
                        <div class="platform-option__info">
                            <span class="platform-option__name">${p.name}</span>
                            <span class="platform-option__size">${version} · ${sizeMB} MB</span>
                        </div>
                    `;
                    dropdownInner.appendChild(btn);
                }
            });
            
            if (dropdownInner.children.length === 0) {
                dropdownInner.innerHTML = `<a href="${data.html_url}" target="_blank" class="platform-option"><div class="platform-option__info"><span class="platform-option__name">View all releases on GitHub</span></div></a>`;
            }
        })
        .catch(err => {
            console.error('Error fetching releases:', err);
            downloadLabel.textContent = 'Download on GitHub';
            downloadBtn.disabled = false;
            downloadBtn.onclick = () => window.open('https://github.com/faizanfatmi/DevInstaller/releases/latest', '_blank');
        });

    // Toggle dropdown
    if (otherBtn && platformDropdown) {
        otherBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            const isHidden = platformDropdown.hidden;
            platformDropdown.hidden = !isHidden;
            otherBtn.setAttribute('aria-expanded', isHidden ? 'true' : 'false');
            if (isHidden) {
                platformDropdown.classList.add('visible');
            } else {
                platformDropdown.classList.remove('visible');
            }
        });

        document.addEventListener('click', (e) => {
            if (!platformDropdown.contains(e.target) && !otherBtn.contains(e.target)) {
                platformDropdown.hidden = true;
                platformDropdown.classList.remove('visible');
                otherBtn.setAttribute('aria-expanded', 'false');
            }
        });
    }
});
