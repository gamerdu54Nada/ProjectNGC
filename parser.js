// ConnectScript Parser
class Parser {
    constructor(code) {
        this.code = code;
        this.lines = code.split('\n').map(l => l.trim()).filter(l => l && !l.startsWith('#'));
        this.currentIndex = 0;
        this.pages = [];
        this.scripts = {};
    }

    parse() {
        try {
            this.parsePages();
            return {
                success: true,
                pages: this.pages,
                scripts: this.scripts,
                error: null
            };
        } catch (e) {
            return {
                success: false,
                pages: [],
                scripts: {},
                error: e.message
            };
        }
    }

    parsePages() {
        for (let i = 0; i < this.lines.length; i++) {
            const line = this.lines[i];
            
            if (line.startsWith('page ')) {
                const pageName = line.substring(5).trim();
                const page = {
                    name: pageName,
                    elements: [],
                    background: { color: 'white' }
                };

                i++;
                while (i < this.lines.length && !this.lines[i].startsWith('page ') && !this.lines[i].startsWith('on ')) {
                    const elementLine = this.lines[i];
                    
                    if (elementLine.startsWith('-background')) {
                        i = this.parseBackground(page, i);
                    } else if (elementLine.startsWith('-button ')) {
                        const buttonName = elementLine.substring(8).trim();
                        const button = { name: buttonName, type: 'button', properties: {} };
                        i = this.parseElement(button, i);
                        page.elements.push(button);
                    } else if (elementLine.startsWith('-text ')) {
                        const textName = elementLine.substring(6).trim();
                        const text = { name: textName, type: 'text', properties: {} };
                        i = this.parseElement(text, i);
                        page.elements.push(text);
                    } else if (elementLine.startsWith('-image ')) {
                        const imageName = elementLine.substring(7).trim();
                        const image = { name: imageName, type: 'image', properties: {} };
                        i = this.parseElement(image, i);
                        page.elements.push(image);
                    }
                    
                    i++;
                }
                
                this.pages.push(page);
                i--;
            } else if (line.startsWith('on ')) {
                const event = line.substring(3).trim();
                const script = { event, actions: [] };
                
                i++;
                while (i < this.lines.length && !this.lines[i].startsWith('end') && !this.lines[i].startsWith('on ')) {
                    script.actions.push(this.parseAction(this.lines[i]));
                    i++;
                }
                
                // Store script by event type for now
                if (!this.scripts[event]) {
                    this.scripts[event] = [];
                }
                this.scripts[event].push(script);
            }
        }
    }

    parseBackground(page, index) {
        index++;
        while (index < this.lines.length && this.lines[index].startsWith('--')) {
            const line = this.lines[index];
            if (line.startsWith('--color ')) {
                page.background.color = line.substring(8).trim();
            }
            index++;
        }
        return index - 1;
    }

    parseElement(element, index) {
        index++;
        while (index < this.lines.length && this.lines[index].startsWith('--')) {
            const line = this.lines[index];
            
            if (line.startsWith('--text ')) {
                element.properties.text = this.extractQuotedValue(line.substring(7));
            } else if (line.startsWith('--value ')) {
                element.properties.value = this.extractQuotedValue(line.substring(8));
            } else if (line.startsWith('--color ')) {
                element.properties.color = line.substring(8).trim();
            } else if (line.startsWith('--position ')) {
                const coords = line.substring(11).trim().split(/\s+/);
                element.properties.position = [parseInt(coords[0]), parseInt(coords[1])];
            } else if (line.startsWith('--size ')) {
                const size = line.substring(7).trim().split(/\s+/);
                element.properties.size = [parseInt(size[0]), parseInt(size[1])];
            } else if (line.startsWith('--fontsize ')) {
                element.properties.fontsize = parseInt(line.substring(11).trim());
            } else if (line.startsWith('--corner ')) {
                element.properties.corner = parseInt(line.substring(9).trim());
            } else if (line.startsWith('--script ')) {
                element.properties.script = line.substring(9).trim();
            } else if (line.startsWith('--source ')) {
                element.properties.source = this.extractQuotedValue(line.substring(9));
            }
            
            index++;
        }
        return index - 1;
    }

    parseAction(line) {
        line = line.trim();
        
        if (line.startsWith('alert(')) {
            const message = this.extractQuotedValue(line.substring(6));
            return { type: 'alert', message };
        } else if (line.startsWith('connect.goto(')) {
            const page = this.extractQuotedValue(line.substring(13));
            return { type: 'goto', page };
        } else if (line.startsWith('play(')) {
            const sound = this.extractQuotedValue(line.substring(5));
            return { type: 'play', sound };
        } else if (line.startsWith('wait(')) {
            const seconds = parseInt(line.substring(5));
            return { type: 'wait', seconds };
        } else if (line.startsWith('set ')) {
            const parts = line.substring(4).split(/\s+/);
            return { type: 'set', variable: parts[0], value: parts[1] };
        } else if (line.startsWith('add ')) {
            const parts = line.substring(4).split(/\s+/);
            return { type: 'add', variable: parts[0], value: parseInt(parts[1]) };
        } else if (line.startsWith('subtract ')) {
            const parts = line.substring(9).split(/\s+/);
            return { type: 'subtract', variable: parts[0], value: parseInt(parts[1]) };
        } else if (line.startsWith('if ')) {
            return { type: 'if', condition: line.substring(3) };
        }
        
        return { type: 'unknown', content: line };
    }

    extractQuotedValue(str) {
        const match = str.match(/"([^"]*)"/);
        return match ? match[1] : str.trim();
    }
}
