// Vue App
const { createApp } = Vue;

createApp({
    components: {
        UIButton: window.UIButton,
        UIText: window.UIText,
        UIImage: window.UIImage
    },
    data() {
        return {
            // Authentication
            isLoggedIn: false,
            currentUser: null,
            loginForm: {
                username: '',
                password: ''
            },
            loginError: '',
            
            // Storage
            storage: null,
            lastSavedTime: null,
            autoSaveEnabled: true,
            unsavedChanges: false,
            storageStats: null,
            // Registration state
            registerMode: false,
            registerForm: { username: '', password: '' },
            registerError: '',
            registerSuccess: '',

            // Explorer state
            pagesExpanded: true,
            scriptsExpanded: true,
            pages: [],
            scriptList: [],
            pageData: {}, // Stores page code
            scripts: {}, // Stores script code

            // Selection state
            selectedItem: { type: null, name: null },
            currentScriptCode: '',
            currentPageCode: '',

            // Runtime state
            runtime: null,
            currentPage: null,
            currentPageData: null,
            parseError: null,
            console: [],
            isRunning: false,
            
            // Backup/Recovery
            showBackupManager: false,
            backupList: [],
            showStorageStats: false
        };
    },

    computed: {
        selectedItemLabel() {
            if (!this.selectedItem || !this.selectedItem.type) return 'Geen selectie';
            return `${this.selectedItem.type === 'page' ? 'Pagina' : 'Script'}: ${this.selectedItem.name || ''}`;
        }
    },

    methods: {
        async login() {
            this.loginError = '';
            const username = this.loginForm.username.trim();
            const password = this.loginForm.password;
            if (!username || !password) { this.loginError = 'Voer gebruikersnaam en wachtwoord in'; return; }

            try {
                const result = await StorageService.verifyAccount(username, password);
                if (!result.success) {
                    this.loginError = result.message || 'Authenticatie mislukt';
                    return;
                }
            } catch (e) {
                this.loginError = 'Fout bij authenticatie';
                return;
            }

            // Success -> initialize session
            this.currentUser = username;
            this.isLoggedIn = true;
            localStorage.setItem('connectedUser', username);
            this.storage = new StorageService(username);
            this.storage.enableAutoSave(() => { this.saveUserProject(); });
            this.loadUserProject();
            this.addLog(`👋 Welkom ${username}! Je bent ingelogd. Auto-save is actief.`, 'success');
        },

        async register() {
            this.registerError = '';
            this.registerSuccess = '';
            const username = this.registerForm.username.trim();
            const password = this.registerForm.password.trim();
            if (!username || !password) { this.registerError = 'Voer gebruikersnaam en wachtwoord in'; return; }
            if (username.length < 3) { this.registerError = 'Gebruikersnaam minimaal 3 karakters'; return; }
            if (password.length < 4) { this.registerError = 'Wachtwoord minimaal 4 karakters'; return; }

            try {
                const res = await StorageService.createAccount(username, password);
                if (res.success) {
                    this.registerSuccess = 'Account aangemaakt. Je kunt nu inloggen.';
                    this.registerForm = { username: '', password: '' };
                    this.registerMode = false;
                } else {
                    this.registerError = res.message || 'Registratie mislukt';
                }
            } catch (e) {
                this.registerError = 'Fout bij registratie';
            }
        },
        
        logout() {
            if (confirm('Wil je echt uitloggen?')) {
                // Save current project before logout
                this.saveUserProject();
                
                // Clear session
                localStorage.removeItem('connectedUser');
                this.isLoggedIn = false;
                this.currentUser = null;
                
                // Clear form
                this.loginForm = {
                    username: '',
                    password: ''
                };
                this.loginError = '';
                
                // Reset editor
                this.pageData = {};
                this.scripts = {};
                this.pages = [];
                this.scriptList = [];
                this.selectedItem = { type: null, name: null };
                this.console = [];
                
                // Log message
                this.addLog('👋 Je bent uitgelogd', 'info');
            }
        },
        
        loadUserProject() {
            // Try to load from storage service
            if (this.storage) {
                const project = this.storage.getProject();
                
                if (project) {
                    this.pageData = project.pages || {};
                    this.scripts = project.scripts || {};
                    this.lastSavedTime = project.lastSaved;
                    
                    // Update UI lists
                    this.pages = Object.keys(this.pageData).map(name => ({ name }));
                    this.scriptList = Object.keys(this.scripts).map(name => ({ name }));
                    
                    // Select first page
                    if (this.pages.length > 0) {
                        this.selectItem('page', this.pages[0].name);
                    }
                    
                    this.addLog(`📂 Project geladen (${this.pages.length} pagina's, ${this.scriptList.length} scripts)`, 'info');
                    return;
                }
            }
            
            // Initialize with default project if not found
            this.initializeProject();
        },
        
        saveUserProject() {
            if (!this.storage) return false;
            
            // Save current item first
            this.saveCurrentItem();
            
            const project = {
                pages: this.pageData,
                scripts: this.scripts
            };
            
            // Save using storage service
            this.storage.saveProject(project).then(success => {
                if (success) {
                    this.lastSavedTime = new Date().toISOString();
                    this.unsavedChanges = false;
                    
                    // Update storage stats
                    this.updateStorageStats();
                    
                    // Create backup periodically
                    if (Math.random() < 0.1) { // 10% chance to create backup
                        this.storage.createBackup(project);
                    }
                }
            });
            
            return true;
        },
        
        // ============ PROJECT METHODS ============
        initializeProject() {
            // Create default pages
            this.pageData['page 1'] = `page 1
-background
--color blue

-text title1
--value "Welkom!"
--color white
--position 50 50
--fontsize 30

-button btn1
--text "Next"
--color green
--script nextScript
--position 100 200
--size 150 50
--corner 10
--fontsize 20`;

            this.pageData['page 2'] = `page 2
-background
--color black

-text title2
--value "Pagina 2"
--color yellow
--position 50 50
--fontsize 30

-button btn2
--text "Back"
--color red
--script backScript
--position 100 200
--size 150 50
--corner 10
--fontsize 20`;

            // Create default scripts referenced by pages
            this.scripts['nextScript'] = `on click
connect.goto(page 2)
end`;

            this.scripts['backScript'] = `on click
connect.goto(page 1)
end`;

            // Update UI lists
            this.pages = Object.keys(this.pageData).map(name => ({ name }));
            this.scriptList = Object.keys(this.scripts).map(name => ({ name }));

            // Select first page by default
            if (this.pages.length > 0) {
                this.selectItem('page', this.pages[0].name);
            }
        },

        togglePagesFolder() {
            this.pagesExpanded = !this.pagesExpanded;
        },

        toggleScriptsFolder() {
            this.scriptsExpanded = !this.scriptsExpanded;
        },

        selectItem(type, name) {
            // Save previous item
            this.saveCurrentItem();

            // Load new item
            this.selectedItem = { type, name };

            if (type === 'page') {
                this.currentPageCode = this.pageData[name] || '';
            } else if (type === 'script') {
                this.currentScriptCode = this.scripts[name] || '';
            }
        },

        saveCurrentItem() {
            if (this.selectedItem.type === 'page' && this.selectedItem.name) {
                this.pageData[this.selectedItem.name] = this.currentPageCode;
            } else if (this.selectedItem.type === 'script' && this.selectedItem.name) {
                this.scripts[this.selectedItem.name] = this.currentScriptCode;
            }
            
            // Mark changes and trigger auto-save
            if (this.storage) {
                this.storage.markChanged();
                this.unsavedChanges = true;
            }
        },

        addNewPage() {
            let pageName = prompt('Voer de paginanaam in:', 'NewPage');
            if (!pageName) return;

            if (this.pageData[pageName]) {
                alert('Pagina bestaat al!');
                return;
            }

            // Create new page
            this.pageData[pageName] = `page ${pageName}
-background
--color white

-text label
--value "${pageName}"
--color black
--position 50 50
--fontsize 24`;

            this.pages.push({ name: pageName });
            this.selectItem('page', pageName);
            this.addLog(`✨ Pagina '${pageName}' aangemaakt`, 'success');
        },

        deletePage(name) {
            if (!confirm(`Verwijder pagina '${name}'?`)) return;
            
            delete this.pageData[name];
            this.pages = this.pages.filter(p => p.name !== name);
            
            // Deselect if deleted
            if (this.selectedItem.name === name) {
                this.selectedItem = { type: null, name: null };
            }
            
            this.addLog(`🗑 Pagina '${name}' verwijderd`, 'warning');
        },

        addNewScript() {
            let scriptName = prompt('Voer de scriptnaam in:', 'MyScript');
            if (!scriptName) return;

            if (this.scripts[scriptName]) {
                alert('Script bestaat al!');
                return;
            }

            // Create new script
            this.scripts[scriptName] = `on click
 alert("Dit is ${scriptName}!")
 # Voeg hier je code toe...
end`;

            this.scriptList.push({ name: scriptName });
            this.selectItem('script', scriptName);
            this.addLog(`✨ Script '${scriptName}' aangemaakt`, 'success');
        },

        addButtonToCurrentPage() {
            // Determine target page
            let pageName = this.selectedItem && this.selectedItem.type === 'page' ? this.selectedItem.name : null;
            if (!pageName) {
                pageName = prompt('Op welke pagina wil je de knop toevoegen? Geef paginanaam op:', Object.keys(this.pageData)[0] || 'page 1');
                if (!pageName) return;
            }

            // Ask for element properties
            const btnName = prompt('Naam van de knop (uniek):', 'btn' + Math.floor(Math.random() * 1000));
            if (!btnName) return;
            if (this.pageData[pageName] && this.pageData[pageName].includes(`button ${btnName}`)) {
                alert('Er bestaat al een element met die naam op de pagina.');
                return;
            }

            const text = prompt('Tekst op de knop:', 'Button');
            const color = prompt('Achtergrondkleur (naam of hex):', 'green');
            const script = prompt('Scriptnaam dat bij klik wordt uitgevoerd (optioneel):', '');
            const posX = prompt('X-positie (px):', '100');
            const posY = prompt('Y-positie (px):', '200');
            const sizeW = prompt('Breedte (px):', '150');
            const sizeH = prompt('Hoogte (px):', '50');
            const corner = prompt('Hoekradius (px):', '6');
            const fontsize = prompt('Tekstgrootte (px):', '14');

            // Build DSL block for the page (Explorer format)
            let block = `\n-button ${btnName}\n--text "${text || ''}"\n--color ${color || ''}\n`;
            if (script) block += `--script ${script}\n`;
            block += `--position ${posX || 100} ${posY || 200}\n--size ${sizeW || 150} ${sizeH || 50}\n--corner ${corner || 6}\n--fontsize ${fontsize || 14}\n`;

            // Append to page text (currentPageCode / pageData)
            if (!this.pageData[pageName]) {
                // create new page skeleton
                this.pageData[pageName] = `page ${pageName}\n-background\n--color white\n\n`;
            }

            // If current page is selected and matches, append to currentPageCode as well
            this.pageData[pageName] = this.pageData[pageName] + block;
            if (this.selectedItem && this.selectedItem.type === 'page' && this.selectedItem.name === pageName) {
                this.currentPageCode = this.pageData[pageName];
            }

            // Ensure page appears in UI lists
            if (!this.pages.find(p => p.name === pageName)) {
                this.pages.push({ name: pageName });
            }

            this.addLog(`➕ Knop '${btnName}' toegevoegd aan pagina '${pageName}'`, 'success');
        },

        insertElementBlock(pageName, block) {
            if (!pageName) return false;
            if (!this.pageData[pageName]) this.pageData[pageName] = `page ${pageName}\n-background\n--color white\n\n`;
            this.pageData[pageName] = this.pageData[pageName] + '\n' + block + '\n';
            if (this.selectedItem && this.selectedItem.type === 'page' && this.selectedItem.name === pageName) {
                this.currentPageCode = this.pageData[pageName];
            }
            if (!this.pages.find(p => p.name === pageName)) this.pages.push({ name: pageName });
            return true;
        },

        deleteScript(name) {
            if (!confirm(`Verwijder script '${name}'?`)) return;
            
            delete this.scripts[name];
            this.scriptList = this.scriptList.filter(s => s.name !== name);
            
            // Deselect if deleted
            if (this.selectedItem.name === name) {
                this.selectedItem = { type: null, name: null };
            }
            
            this.addLog(`🗑 Script '${name}' verwijderd`, 'warning');
        },

        runCode() {
            this.console = [];
            this.parseError = null;
            
            // Save current item first
            this.saveCurrentItem();
            
            // Combine all code
            const allPageCode = Object.values(this.pageData).join('\n\n');
            const allScriptCode = Object.values(this.scripts).join('\n\n');
            const fullCode = allPageCode + '\n\n' + allScriptCode;
            
            // Parse code
            const parser = new Parser(fullCode);
            const result = parser.parse();
            
            if (!result.success) {
                this.parseError = result.error;
                this.addLog(`❌ Parse Error: ${result.error}`, 'error');
                return;
            }
            
            // Initialize runtime
            this.runtime = new Runtime(
                result,
                (msg, type) => this.addLog(msg, type),
                (pageName) => this.switchPage(pageName)
            );
            
            this.runtime.initialize();
            this.addLog('✅ App gestart!', 'success');
            
            // Set first page
            if (result.pages.length > 0) {
                this.switchPage(result.pages[0].name);
            }
        },

        switchPage(pageName) {
            if (!this.runtime) return;
            
            this.currentPage = pageName;
            this.currentPageData = this.runtime.getCurrentPageData();
            this.addLog(`📍 Pagina: ${pageName}`, 'info');
        },

        handleElementClick(element) {
            if (!this.runtime) return;
            
            if (element.type === 'button') {
                this.addLog(`🔘 Klik: ${element.name}`, 'info');
                this.runtime.onClick(element.name);
            }
        },

        getBackground(page) {
            return page.background ? page.background.color : '#ffffff';
        },

        addLog(message, type = 'info') {
            this.console.push({ message, type });
            
            // Auto-scroll console
            this.$nextTick(() => {
                const consoleEl = document.querySelector('.console');
                if (consoleEl) {
                    consoleEl.scrollTop = consoleEl.scrollHeight;
                }
            });
        },

        clearConsole() {
            this.console = [];
        },

        clearAllData() {
            if (confirm('Wil je alles resetten? Dit verwijdert alle pagina\'s en scripts!')) {
                this.pageData = {};
                this.scripts = {};
                this.pages = [];
                this.scriptList = [];
                this.selectedItem = { type: null, name: null };
                this.console = [];
                this.initializeProject();
                this.addLog('🔄 Project gereset', 'info');
            }
        },

        handleEditorKeydown(e) {
            if (e.key === 'Tab') {
                e.preventDefault();
                const textarea = e.target;
                const start = textarea.selectionStart;
                const end = textarea.selectionEnd;
                
                if (this.selectedItem.type === 'page') {
                    this.currentPageCode = this.currentPageCode.substring(0, start) + '\t' + this.currentPageCode.substring(end);
                } else if (this.selectedItem.type === 'script') {
                    this.currentScriptCode = this.currentScriptCode.substring(0, start) + '\t' + this.currentScriptCode.substring(end);
                }
                
                this.$nextTick(() => {
                    textarea.selectionStart = textarea.selectionEnd = start + 1;
                });
            }
        },

        downloadProject() {
            const data = {
                pages: this.pageData,
                scripts: this.scripts,
                timestamp: new Date().toISOString()
            };
            
            const element = document.createElement('a');
            element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(JSON.stringify(data, null, 2)));
            element.setAttribute('download', 'connectscript_project.json');
            element.style.display = 'none';
            
            document.body.appendChild(element);
            element.click();
            document.body.removeChild(element);
            
            this.addLog('💾 Project gedownload!', 'success');
        },
        
        exportScriptsToHTML() {
            let scriptsArray = [];
            if (this.scriptList && this.scriptList.length > 0) {
                scriptsArray = this.scriptList.map(s => ({ name: s.name, code: this.scripts && this.scripts[s.name] ? this.scripts[s.name] : '' }));
            } else if (this.scripts && Object.keys(this.scripts).length > 0) {
                scriptsArray = Object.keys(this.scripts).map(name => ({ name, code: this.scripts[name] }));
            }
            if (scriptsArray.length === 0) {
                this.addLog('❌ Geen scripts om te exporteren', 'error');
                return;
            }

            const timestamp = new Date().toLocaleString('nl-NL');
            const scriptsList = scriptsArray.map(s => `
        <div class="script-section">
            <h3>📄 ${this.escapeHtml(s.name)}</h3>
            <pre class="script-code"><code>${this.escapeHtml(s.code)}</code></pre>
        </div>`).join('');
            
            const html = `<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ConnectScript - Exported Scripts</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            padding: 30px;
        }
        
        .header {
            border-bottom: 3px solid #667eea;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        
        h1 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 28px;
        }
        
        .meta-info {
            color: #7f8c8d;
            font-size: 13px;
        }
        
        .meta-info span {
            margin-right: 20px;
            display: inline-block;
        }
        
        .script-section {
            margin-bottom: 30px;
            border: 1px solid #ecf0f1;
            border-radius: 8px;
            overflow: hidden;
        }
        
        .script-section h3 {
            background: #f8f9fa;
            color: #2c3e50;
            padding: 15px;
            margin: 0;
            font-size: 16px;
            border-bottom: 1px solid #ecf0f1;
        }
        
        .script-code {
            background: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            line-height: 1.5;
            margin: 0;
            border-radius: 0;
        }
        
        .script-code code {
            font-family: inherit;
        }
        
        .footer {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ecf0f1;
            color: #7f8c8d;
            font-size: 12px;
            text-align: center;
        }
        
        @media print {
            body {
                background: white;
            }
            .container {
                box-shadow: none;
                border: none;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎨 ConnectScript - Scripts</h1>
            <div class="meta-info">
                <span>👤 User: ${this.escapeHtml(this.currentUser)}</span>
                <span>📅 Exported: ${timestamp}</span>
                <span>📊 Scripts: ${scriptsArray.length}</span>
            </div>
        </div>
        
        <div class="scripts-container">${scriptsList}
        </div>
        
        <div class="footer">
            <p>Generated by ConnectScript Studio</p>
            <p><small>For more information, visit the ConnectScript documentation</small></p>
        </div>
    </div>
</body>
</html>`;
            
            const element = document.createElement('a');
            element.setAttribute('href', 'data:text/html;charset=utf-8,' + encodeURIComponent(html));
            element.setAttribute('download', `connectscript_scripts_${new Date().getTime()}.html`);
            element.style.display = 'none';
            
            document.body.appendChild(element);
            element.click();
            document.body.removeChild(element);
            
            this.addLog(`📄 ${scriptsArray.length} script(s) als HTML geëxporteerd!`, 'success');
        },

                exportPreviewToHTML() {
                        try {
                                const page = this.currentPageData || (this.currentPage && this.pageData[this.currentPage]);
                                if (!page) {
                                        this.addLog('❌ Geen preview beschikbaar om te exporteren', 'error');
                                        return;
                                }

                                const bg = this.getBackground(page) || '#ffffff';
                                const elements = page.elements || [];

                                const elementsHtml = elements.map(el => {
                                        const left = (el.properties && el.properties.position && el.properties.position[0]) ? el.properties.position[0] : 10;
                                        const top = (el.properties && el.properties.position && el.properties.position[1]) ? el.properties.position[1] : 10;
                                        const width = (el.properties && el.properties.size && el.properties.size[0]) ? el.properties.size[0] : 120;
                                        const height = (el.properties && el.properties.size && el.properties.size[1]) ? el.properties.size[1] : (el.type === 'text' ? 'auto' : 40);
                                        if (el.type === 'button') {
                                                const text = (el.properties && (el.properties.text || el.properties.value)) ? (el.properties.text || el.properties.value) : 'Button';
                                                const color = el.properties && el.properties.color ? el.properties.color : '#007bff';
                                                const textColor = el.properties && el.properties.textColor ? el.properties.textColor : '#ffffff';
                                                const corner = el.properties && el.properties.corner ? el.properties.corner : 4;
                                                return `<button style="position:absolute; left:${left}px; top:${top}px; width:${width}px; height:${height}px; background:${color}; color:${textColor}; border:none; border-radius:${corner}px; font-size:${(el.properties && el.properties.fontsize) || 14}px;">${this.escapeHtml(text)}</button>`;
                                        } else if (el.type === 'text') {
                                                const value = el.properties && el.properties.value ? el.properties.value : '';
                                                const color = el.properties && el.properties.color ? el.properties.color : '#000';
                                                const fontSize = el.properties && el.properties.fontsize ? el.properties.fontsize : 16;
                                                return `<div style="position:absolute; left:${left}px; top:${top}px; color:${color}; font-size:${fontSize}px;">${this.escapeHtml(value)}</div>`;
                                        } else {
                                                const src = el.properties && el.properties.source ? el.properties.source : '';
                                                return `<img src="${this.escapeHtml(src)}" style="position:absolute; left:${left}px; top:${top}px; width:${width}px; height:${height}px; object-fit:cover;" />`;
                                        }
                                }).join('\n');

                                const title = this.currentPage || 'Preview';
                                const timestamp = new Date().toLocaleString('nl-NL');

                                const html = `<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>ConnectScript - ${this.escapeHtml(title)}</title>
    <style>
        body { margin:0; font-family: Arial, Helvetica, sans-serif; background:${bg}; }
        .canvas { position: relative; width: 100%; height: 100vh; background: ${bg}; overflow: hidden; }
    </style>
</head>
<body>
    <div class="canvas">
        ${elementsHtml}
    </div>
    <footer style="position:fixed; left:10px; bottom:10px; color:#666; font-size:12px;">Exported: ${timestamp}</footer>
</body>
</html>`;

                                const element = document.createElement('a');
                                element.setAttribute('href', 'data:text/html;charset=utf-8,' + encodeURIComponent(html));
                                element.setAttribute('download', `connectscript_preview_${(this.currentPage || 'preview')}_${Date.now()}.html`);
                                element.style.display = 'none';
                                document.body.appendChild(element);
                                element.click();
                                document.body.removeChild(element);

                                this.addLog(`🌐 Preview geëxporteerd: ${this.currentPage || 'preview'}`, 'success');
                        } catch (err) {
                                this.addLog('❌ Fout bij exporteren preview: ' + (err && err.message ? err.message : String(err)), 'error');
                                console.error(err);
                        }
                },
        
        escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        },
        
        // ============ BACKUP & RECOVERY ============
        
        createBackupNow() {
            if (!this.storage) return;
            
            this.saveCurrentItem();
            const project = {
                pages: this.pageData,
                scripts: this.scripts
            };
            
            this.storage.createBackup(project);
            this.backupList = this.storage.getBackups();
            this.addLog(`✅ Backup gemaakt! (${this.backupList.length} beschikbaar)`, 'success');
        },
        
        showBackupManagerDialog() {
            this.backupList = this.storage ? this.storage.getBackups() : [];
            this.showBackupManager = true;
        },
        
        restoreFromBackup(timestamp) {
            if (!this.storage) return;
            
            if (confirm('Wil je van deze backup herstellen? Huidige werk gaat verloren!')) {
                const project = this.storage.restoreBackup(timestamp);
                
                if (project) {
                    this.pageData = project.pages || {};
                    this.scripts = project.scripts || {};
                    
                    this.pages = Object.keys(this.pageData).map(name => ({ name }));
                    this.scriptList = Object.keys(this.scripts).map(name => ({ name }));
                    
                    if (this.pages.length > 0) {
                        this.selectItem('page', this.pages[0].name);
                    }
                    
                    this.showBackupManager = false;
                    this.addLog('✅ Hersteld vanuit backup!', 'success');
                } else {
                    this.addLog('❌ Backup kon niet worden hersteld', 'error');
                }
            }
        },
        
        deleteBackup(timestamp) {
            if (confirm('Verwijder deze backup?')) {
                const backups = this.storage.getBackups();
                const filtered = backups.filter(b => b.timestamp !== timestamp);
                
                localStorage.setItem(
                    `connectedScript_backup_${this.currentUser}`,
                    JSON.stringify(filtered)
                );
                
                this.backupList = filtered;
                this.addLog('🗑️ Backup verwijderd', 'info');
            }
        },
        
        updateStorageStats() {
            if (!this.storage) return;
            this.storageStats = this.storage.getStorageStats();
        },
        
        showStorageStatsDialog() {
            this.updateStorageStats();
            // Attach keydown handler to allow Escape to close the modal
            if (!this._storageStatsKeyHandler) {
                this._storageStatsKeyHandler = (e) => {
                    if (e.key === 'Escape' || e.key === 'Esc') {
                        this.closeStorageStats();
                    }
                };
            }
            document.addEventListener('keydown', this._storageStatsKeyHandler);
            this.showStorageStats = true;
        },

        closeStorageStats() {
            this.showStorageStats = false;
            // remove key handler
            if (this._storageStatsKeyHandler) {
                document.removeEventListener('keydown', this._storageStatsKeyHandler);
            }
        },
        
        clearOldBackups() {
            if (!this.storage) return;
            
            const removed = this.storage.clearOldBackups(30);
            if (removed > 0) {
                this.backupList = this.storage.getBackups();
                this.addLog(`🧹 ${removed} oude backups verwijderd`, 'info');
            } else {
                this.addLog('Geen oude backups om te verwijderen', 'info');
            }

        }
    }
}).mount('#app');
