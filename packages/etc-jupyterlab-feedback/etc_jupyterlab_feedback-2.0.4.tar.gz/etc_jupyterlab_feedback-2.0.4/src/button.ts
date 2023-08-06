export interface IETCJupyterLabConfigurableTextButtonOptions {
    stylePressed: any;
    style: any;
    innerHTML: string;
}

export class ETCJupyterLabConfigurableTextButton {

    public eventTarget: EventTarget;
    public button: HTMLButtonElement;
    public node: HTMLElement;

    private _style: any;
    private _stylePressed: any;
    private _span: HTMLElement;

    constructor({
        stylePressed,
        style,
        innerHTML
    }: IETCJupyterLabConfigurableTextButtonOptions) {

        this._stylePressed = stylePressed;
        this._style = style;

        this.eventTarget = new EventTarget();

        let node = this.node = document.createElement('div');
        let button = this.button = document.createElement('button');
        button.classList.add('jp-Button');
        let span = this._span = document.createElement('span');
        span.classList.add('bp3-button-text');

        if (innerHTML) {
            span.innerHTML = innerHTML;
        }

        button.appendChild(span);
        node.appendChild(button);

        if (style) {
            Object.assign(button.style, style);
        }

        this.enable();
    }

    public disable() {
        this.button.removeEventListener('mousedown', this);
        this.button.removeEventListener('mouseup', this);
        this.button.removeEventListener('click', this);
    }

    public enable() {
        this.button.addEventListener('mousedown', this);
        this.button.addEventListener('mouseup', this);
        this.button.addEventListener('click', this);
    }

    public handleEvent(event: Event) {

        try {
            if (event.type == 'click') {
                this.eventTarget.dispatchEvent(new CustomEvent('click'));
            }
            else if (event.type == 'mousedown') {
                Object.assign(this.button.style, this._stylePressed);
                document.addEventListener('mouseup', this, { once: true });
            }
            else if (event.type == 'mouseup') {
                Object.assign(this.button.style, this._style);
            }
        }
        catch (e) {
            console.error(e);
        }
    }

    set innerHtml(html: string) {
        this._span.innerHTML = html;
    }
}