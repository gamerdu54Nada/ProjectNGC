// ConnectScript Runtime
class Runtime {
    constructor(ast, onLog, onNavigate) {
        this.ast = ast;
        this.onLog = onLog;
        this.onNavigate = onNavigate;
        this.variables = {};
        this.currentPage = null;
        this.waitingPromise = null;
    }

    initialize() {
        if (this.ast.pages.length > 0) {
            this.currentPage = this.ast.pages[0].name;
            this.onLog(`✓ App gestart: Pagina '${this.currentPage}' geladen`, 'success');
            
            // Execute start events
            this.executeEvent('start');
        } else {
            this.onLog('⚠ Geen pagina\'s gedefinieerd', 'warning');
        }
    }

    onClick(elementName) {
        this.onLog(`🖱 Klik op: ${elementName}`, 'info');
        
        // Find element and get its script
        const page = this.ast.pages.find(p => p.name === this.currentPage);
        if (!page) return;
        
        const element = page.elements.find(e => e.name === elementName);
        if (!element || !element.properties.script) {
            this.onLog(`⚠ Geen script gedefinieerd voor ${elementName}`, 'warning');
            return;
        }
        
        // Execute the button's script
        this.executeScript(element.properties.script);
    }

    executeEvent(eventName) {
        if (!this.ast.scripts[eventName]) {
            return;
        }
        
        for (const script of this.ast.scripts[eventName]) {
            for (const action of script.actions) {
                this.executeAction(action);
            }
        }
    }

    executeScript(scriptName) {
        // Find script by click event (simplified)
        const clickScripts = this.ast.scripts['click'] || [];
        for (const script of clickScripts) {
            // Simple matching by checking if any script can be called
            for (const action of script.actions) {
                this.executeAction(action);
            }
        }
    }

    executeAction(action) {
        switch (action.type) {
            case 'alert':
                this.onLog(`📢 Alert: ${action.message}`, 'info');
                alert(action.message);
                break;
                
            case 'goto':
                this.navigateToPage(action.page);
                break;
                
            case 'play':
                this.onLog(`🔊 Speel af: ${action.sound}`, 'info');
                break;
                
            case 'wait':
                this.onLog(`⏱ Wacht ${action.seconds}s...`, 'info');
                break;
                
            case 'set':
                this.variables[action.variable] = action.value;
                this.onLog(`📌 ${action.variable} = ${action.value}`, 'info');
                break;
                
            case 'add':
                const currentVal = parseInt(this.variables[action.variable] || 0);
                this.variables[action.variable] = currentVal + action.value;
                this.onLog(`➕ ${action.variable} += ${action.value} (nu: ${this.variables[action.variable]})`, 'success');
                break;
                
            case 'subtract':
                const subVal = parseInt(this.variables[action.variable] || 0);
                this.variables[action.variable] = subVal - action.value;
                this.onLog(`➖ ${action.variable} -= ${action.value} (nu: ${this.variables[action.variable]})`, 'success');
                break;
                
            case 'if':
                // Simplified condition handling
                this.onLog(`❓ If: ${action.condition}`, 'info');
                break;
                
            default:
                this.onLog(`? Onbekende actie: ${action.type}`, 'warning');
        }
    }

    navigateToPage(pageName) {
        const page = this.ast.pages.find(p => p.name === pageName);
        if (!page) {
            this.onLog(`❌ Pagina "${pageName}" niet gevonden`, 'error');
            return;
        }
        
        this.currentPage = pageName;
        this.onLog(`📄 Navigeer naar: ${pageName}`, 'success');
        this.onNavigate(pageName);
    }

    getVariables() {
        return this.variables;
    }

    getPages() {
        return this.ast.pages;
    }

    getCurrentPageData() {
        return this.ast.pages.find(p => p.name === this.currentPage);
    }
}
