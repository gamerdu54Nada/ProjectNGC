/**
 * Storage Service
 * Handles all data persistence with multiple backup strategies
 */

class StorageService {
    constructor(username) {
        this.username = username;
        this.projectKey = `connectedScript_${username}`;
        this.backupKey = `connectedScript_backup_${username}`;
        this.historyKey = `connectedScript_history_${username}`;
        this.metaKey = `connectedScript_meta_${username}`;
        
        // Auto-save interval (5 seconds)
        this.autoSaveInterval = 5000;
        this.autoSaveTimer = null;
        this.hasUnsavedChanges = false;
        
        // Initialize IndexedDB for large storage
        this.initDB();
    }
    
    /**
     * Initialize IndexedDB database
     */
    async initDB() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open('ConnectScriptDB', 3);
            
            request.onerror = () => reject(request.error);
            request.onsuccess = () => {
                this.db = request.result;
                resolve();
            };
            
            request.onupgradeneeded = (event) => {
                const db = event.target.result;
                if (!db.objectStoreNames.contains('projects')) {
                    db.createObjectStore('projects', { keyPath: 'username' });
                }
                if (!db.objectStoreNames.contains('backups')) {
                    db.createObjectStore('backups', { keyPath: 'id', autoIncrement: true });
                }
                if (!db.objectStoreNames.contains('accounts')) {
                    db.createObjectStore('accounts', { keyPath: 'username' });
                }
                if (!db.objectStoreNames.contains('messages')) {
                    db.createObjectStore('messages', { keyPath: 'id', autoIncrement: true });
                }
            };
        });
    }
    
    /**
     * Get current project data
     */
    getProject() {
        const data = localStorage.getItem(this.projectKey);
        if (!data) return null;
        
        try {
            return JSON.parse(data);
        } catch (e) {
            console.error('Fout bij laden project:', e);
            return null;
        }
    }
    
    /**
     * Save project to localStorage + IndexedDB
     */
    async saveProject(project) {
        try {
            // Save to localStorage (primary)
            const projectData = {
                username: this.username,
                pages: project.pages || {},
                scripts: project.scripts || {},
                lastSaved: new Date().toISOString(),
                version: this.getMetadata().version || 1
            };
            
            localStorage.setItem(this.projectKey, JSON.stringify(projectData));
            
            // Save to IndexedDB (backup)
            if (this.db) {
                await this.saveToIndexedDB('projects', projectData);
            }
            
            // Update metadata
            this.updateMetadata({
                lastSaved: new Date().toISOString(),
                size: JSON.stringify(projectData).length
            });
            
            // Create history entry
            await this.addToHistory(projectData);
            
            // Mark as saved
            this.hasUnsavedChanges = false;
            
            return true;
        } catch (e) {
            console.error('Fout bij opslaan project:', e);
            return false;
        }
    }
    
    /**
     * Mark that changes have been made
     */
    markChanged() {
        this.hasUnsavedChanges = true;
    }
    
    /**
     * Enable auto-save
     */
    enableAutoSave(saveCallback) {
        this.autoSaveTimer = setInterval(() => {
            if (this.hasUnsavedChanges && saveCallback) {
                saveCallback();
            }
        }, this.autoSaveInterval);
    }
    
    /**
     * Disable auto-save
     */
    disableAutoSave() {
        if (this.autoSaveTimer) {
            clearInterval(this.autoSaveTimer);
            this.autoSaveTimer = null;
        }
    }
    
    /**
     * Create backup
     */
    async createBackup(project) {
        try {
            const backup = {
                username: this.username,
                data: project,
                timestamp: new Date().toISOString(),
                version: this.getMetadata().version || 1
            };
            
            // Save to localStorage backup
            const backups = this.getBackups();
            backups.push(backup);
            
            // Keep only last 10 backups
            if (backups.length > 10) {
                backups.shift();
            }
            
            localStorage.setItem(this.backupKey, JSON.stringify(backups));
            
            // Save to IndexedDB
            if (this.db) {
                await this.saveToIndexedDB('backups', backup);
            }
            
            return true;
        } catch (e) {
            console.error('Fout bij backup:', e);
            return false;
        }
    }
    
    /**
     * Get all backups
     */
    getBackups() {
        const data = localStorage.getItem(this.backupKey);
        if (!data) return [];
        
        try {
            return JSON.parse(data);
        } catch (e) {
            return [];
        }
    }
    
    /**
     * Restore from backup
     */
    restoreBackup(timestamp) {
        const backups = this.getBackups();
        const backup = backups.find(b => b.timestamp === timestamp);
        
        if (backup) {
            localStorage.setItem(this.projectKey, JSON.stringify(backup.data));
            return backup.data;
        }
        
        return null;
    }
    
    /**
     * Add to history
     */
    async addToHistory(project) {
        try {
            const history = this.getHistory();
            
            history.push({
                timestamp: new Date().toISOString(),
                version: this.getMetadata().version || 1,
                pages: Object.keys(project.pages || {}).length,
                scripts: Object.keys(project.scripts || {}).length
            });
            
            // Keep only last 50 history entries
            if (history.length > 50) {
                history.shift();
            }
            
            localStorage.setItem(this.historyKey, JSON.stringify(history));
        } catch (e) {
            console.error('Fout bij history:', e);
        }
    }
    
    /**
     * Get history
     */
    getHistory() {
        const data = localStorage.getItem(this.historyKey);
        if (!data) return [];
        
        try {
            return JSON.parse(data);
        } catch (e) {
            return [];
        }
    }
    
    /**
     * Update metadata
     */
    updateMetadata(updates) {
        const meta = this.getMetadata();
        const updated = {
            ...meta,
            ...updates,
            lastUpdated: new Date().toISOString()
        };
        
        localStorage.setItem(this.metaKey, JSON.stringify(updated));
    }
    
    /**
     * Get metadata
     */
    getMetadata() {
        const data = localStorage.getItem(this.metaKey);
        if (!data) return {};
        
        try {
            return JSON.parse(data);
        } catch (e) {
            return {};
        }
    }
    
    /**
     * Save to IndexedDB
     */
    async saveToIndexedDB(storeName, data) {
        return new Promise((resolve, reject) => {
            if (!this.db) {
                reject('IndexedDB not available');
                return;
            }
            
            const transaction = this.db.transaction([storeName], 'readwrite');
            const objectStore = transaction.objectStore(storeName);
            const request = objectStore.put(data);
            
            request.onerror = () => reject(request.error);
            request.onsuccess = () => resolve(request.result);
        });
    }
    
    /**
     * Export project as JSON
     */
    exportProject(project) {
        const data = {
            name: `ConnectScript_${this.username}`,
            exportDate: new Date().toISOString(),
            format: 'json',
            version: '1.0',
            project: project
        };
        
        return JSON.stringify(data, null, 2);
    }
    
    /**
     * Clear old data
     */
    clearOldBackups(daysOld = 30) {
        const backups = this.getBackups();
        const cutoffDate = new Date();
        cutoffDate.setDate(cutoffDate.getDate() - daysOld);
        
        const filtered = backups.filter(b => {
            return new Date(b.timestamp) > cutoffDate;
        });
        
        if (filtered.length < backups.length) {
            localStorage.setItem(this.backupKey, JSON.stringify(filtered));
            return backups.length - filtered.length;
        }
        
        return 0;
    }
    
    /**
     * Get storage stats
     */
    getStorageStats() {
        const project = this.getProject();
        const backups = this.getBackups();
        const history = this.getHistory();
        
        const projectSize = project ? JSON.stringify(project).length : 0;
        const backusSize = JSON.stringify(backups).length;
        const historySize = JSON.stringify(history).length;
        
        return {
            projectSize: this.formatBytes(projectSize),
            backupSize: this.formatBytes(backusSize),
            historySize: this.formatBytes(historySize),
            totalSize: this.formatBytes(projectSize + backusSize + historySize),
            backupCount: backups.length,
            historyEntries: history.length
        };
    }
    
    /**
     * Format bytes to human readable
     */
    formatBytes(bytes) {
        if (bytes === 0) return '0 B';
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
    }
    
    /**
     * Cleanup
     */
    destroy() {
        this.disableAutoSave();
        if (this.db) {
            this.db.close();
        }
    }
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = StorageService;
}

// ----- Static account helpers -----
// Uses the same IndexedDB database to store user accounts (username, salt, hash)
StorageService.openDB = function() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open('ConnectScriptDB', 3);
        request.onerror = () => reject(request.error);
        request.onsuccess = () => resolve(request.result);
        request.onupgradeneeded = (event) => {
            const db = event.target.result;
            if (!db.objectStoreNames.contains('projects')) db.createObjectStore('projects', { keyPath: 'username' });
            if (!db.objectStoreNames.contains('backups')) db.createObjectStore('backups', { keyPath: 'id', autoIncrement: true });
            if (!db.objectStoreNames.contains('accounts')) db.createObjectStore('accounts', { keyPath: 'username' });
            if (!db.objectStoreNames.contains('messages')) db.createObjectStore('messages', { keyPath: 'id', autoIncrement: true });
        };
    });
};

StorageService.hashPassword = async function(password, salt) {
    const enc = new TextEncoder();
    const pwBytes = enc.encode(password);
    const combined = new Uint8Array(salt.length + pwBytes.length);
    combined.set(salt, 0);
    combined.set(pwBytes, salt.length);
    const hashBuf = await crypto.subtle.digest('SHA-256', combined);
    return new Uint8Array(hashBuf);
};

StorageService._toBase64 = function(buf) {
    let binary = '';
    const bytes = new Uint8Array(buf);
    const len = bytes.byteLength;
    for (let i = 0; i < len; i++) binary += String.fromCharCode(bytes[i]);
    return btoa(binary);
};

StorageService._fromBase64 = function(str) {
    const binary = atob(str);
    const len = binary.length;
    const bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++) bytes[i] = binary.charCodeAt(i);
    return bytes;
};

StorageService.createAccount = async function(username, password) {
    if (!username || !password) throw new Error('Invalid input');
    const db = await StorageService.openDB();
    return new Promise((resolve, reject) => {
        const tx = db.transaction(['accounts'], 'readwrite');
        const store = tx.objectStore('accounts');
        const getReq = store.get(username);
        getReq.onsuccess = async () => {
            if (getReq.result) {
                resolve({ success: false, message: 'Gebruikersnaam bestaat al' });
                return;
            }

            // create salt
            const salt = crypto.getRandomValues(new Uint8Array(16));
            const hash = await StorageService.hashPassword(password, salt);

            const record = {
                username,
                salt: StorageService._toBase64(salt),
                hash: StorageService._toBase64(hash),
                createdAt: new Date().toISOString()
            };

            const addReq = store.add(record);
            addReq.onsuccess = () => resolve({ success: true });
            addReq.onerror = () => resolve({ success: false, message: addReq.error?.message || 'DB error' });
        };
        getReq.onerror = () => resolve({ success: false, message: getReq.error?.message || 'DB error' });
    });
};

StorageService.getAccount = async function(username) {
    const db = await StorageService.openDB();
    return new Promise((resolve, reject) => {
        const tx = db.transaction(['accounts'], 'readonly');
        const store = tx.objectStore('accounts');
        const req = store.get(username);
        req.onsuccess = () => resolve(req.result || null);
        req.onerror = () => reject(req.error);
    });
};

StorageService.verifyAccount = async function(username, password) {
    const acct = await StorageService.getAccount(username);
    if (!acct) return { success: false, message: 'Gebruiker niet gevonden' };
    const salt = StorageService._fromBase64(acct.salt);
    const expectedHash = StorageService._fromBase64(acct.hash);
    const hash = await StorageService.hashPassword(password, salt);
    // compare
    if (hash.length !== expectedHash.length) return { success: false, message: 'Ongeldig wachtwoord' };
    let equal = true;
    for (let i = 0; i < hash.length; i++) if (hash[i] !== expectedHash[i]) { equal = false; break; }
    return equal ? { success: true } : { success: false, message: 'Ongeldig wachtwoord' };
};

// Admin functions
StorageService.getAllAccounts = async function() {
    const db = await StorageService.openDB();
    return new Promise((resolve, reject) => {
        const tx = db.transaction(['accounts'], 'readonly');
        const store = tx.objectStore('accounts');
        const req = store.getAll();
        req.onsuccess = () => {
            const accounts = req.result.map(acc => ({
                username: acc.username,
                createdAt: acc.createdAt
            }));
            resolve(accounts);
        };
        req.onerror = () => reject(req.error);
    });
};

StorageService.getAllProjects = async function() {
    const db = await StorageService.openDB();
    return new Promise((resolve, reject) => {
        const tx = db.transaction(['projects'], 'readonly');
        const store = tx.objectStore('projects');
        const req = store.getAll();
        req.onsuccess = () => {
            const projects = req.result.map(proj => ({
                username: proj.username,
                lastSaved: proj.lastSaved,
                pagesCount: Object.keys(proj.pages || {}).length,
                scriptsCount: Object.keys(proj.scripts || {}).length,
                data: proj
            }));
            resolve(projects);
        };
        req.onerror = () => reject(req.error);
    });
};

// Chat functions
StorageService.prototype.saveMessage = async function(conversation, senderUsername, message) {
    if (!this.db) return false;
    
    // Create conversation ID (sorted usernames to ensure uniqueness)
    const participants = [this.username, conversation].sort();
    const convId = participants.join('_');
    
    return new Promise((resolve) => {
        const tx = this.db.transaction(['messages'], 'readwrite');
        const store = tx.objectStore('messages');
        
        const msg = {
            conversationId: convId,
            sender: senderUsername,
            text: message,
            timestamp: new Date().toISOString()
        };
        
        const req = store.add(msg);
        req.onsuccess = () => resolve(true);
        req.onerror = () => resolve(false);
    });
};

StorageService.prototype.getMessages = async function(otherUsername) {
    if (!this.db) return [];
    
    const participants = [this.username, otherUsername].sort();
    const convId = participants.join('_');
    
    return new Promise((resolve) => {
        const tx = this.db.transaction(['messages'], 'readonly');
        const store = tx.objectStore('messages');
        const req = store.getAll();
        
        req.onsuccess = () => {
            const msgs = req.result
                .filter(m => m.conversationId === convId)
                .sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
            resolve(msgs);
        };
        req.onerror = () => resolve([]);
    });
};

StorageService.prototype.getConversations = async function() {
    if (!this.db) return [];
    
    return new Promise((resolve) => {
        const tx = this.db.transaction(['messages'], 'readonly');
        const store = tx.objectStore('messages');
        const req = store.getAll();
        
        req.onsuccess = () => {
            const convMap = {};
            req.result.forEach(msg => {
                const parts = msg.conversationId.split('_');
                const otherUser = parts[0] === this.username ? parts[1] : parts[0];
                
                if (!convMap[msg.conversationId]) {
                    convMap[msg.conversationId] = {
                        conversationId: msg.conversationId,
                        otherUser,
                        lastMessage: msg.text,
                        lastTimestamp: msg.timestamp,
                        messageCount: 0
                    };
                }
                convMap[msg.conversationId].messageCount++;
                convMap[msg.conversationId].lastTimestamp = msg.timestamp;
                convMap[msg.conversationId].lastMessage = msg.text;
            });
            
            resolve(Object.values(convMap).sort((a, b) => 
                new Date(b.lastTimestamp) - new Date(a.lastTimestamp)
            ));
        };
        req.onerror = () => resolve([]);
    });
};

StorageService.getAllConversations = async function() {
    const db = await StorageService.openDB();
    return new Promise((resolve) => {
        const tx = db.transaction(['messages'], 'readonly');
        const store = tx.objectStore('messages');
        const req = store.getAll();
        
        req.onsuccess = () => {
            const convMap = {};
            req.result.forEach(msg => {
                if (!convMap[msg.conversationId]) {
                    const parts = msg.conversationId.split('_');
                    convMap[msg.conversationId] = {
                        conversationId: msg.conversationId,
                        participants: parts,
                        messageCount: 0,
                        messages: []
                    };
                }
                convMap[msg.conversationId].messageCount++;
                convMap[msg.conversationId].messages.push({
                    sender: msg.sender,
                    text: msg.text,
                    timestamp: msg.timestamp
                });
            });
            
            resolve(Object.values(convMap));
        };
        req.onerror = () => resolve([]);
    });
};
