import { FunctionComponent, useEffect, useMemo, useRef, useState } from 'react';
import FigInterface from './FigInterface';
import QueryParameters from './QueryParameters';
import randomAlphaString from './util/randomAlphaString';
import urlFromUri from './util/urlFromUri';

type Props = {
    model: WidgetModel
    viewUri: string
    dataUri: string
    height: number
}

const parentOrigin = window.location.protocol + '//' + window.location.host
import createElectronInterface from './createElectronInterface'
import { WidgetModel } from '@jupyter-widgets/base';
import { sleepMsec } from './sleepMsec';

const FigureWidget: FunctionComponent<Props> = ({model, viewUri, dataUri, height}) => {
    const [width, setWidth] = useState<number | undefined>(undefined)
    const iframeElement = useRef<HTMLIFrameElement | null>()
    const viewUrlBase = urlFromUri(viewUri)
    const viewUrl = viewUrlBase + '/index.html'
    const [figInterface, setFigInterface] = useState<FigInterface | undefined>(undefined)
    // we need a unique figure ID for each figure interface
    const figureId = useMemo(() => (randomAlphaString(10)), [])
    const src = useMemo(() => {
        let ret = `${viewUrl}?parentOrigin=${parentOrigin}&figureId=${figureId}`
        return ret
    }, [parentOrigin, viewUrl])
    useEffect(() => {
        const queryParameters: QueryParameters = {
            viewUri,
            dataUri
        }
        const electronInterface = createElectronInterface(model)
        const figInterface = new FigInterface({ electronInterface, figureId, iframeElement })
        figInterface.initialize(queryParameters).then(() => {
            setFigInterface(figInterface)
        })
    }, [viewUri, dataUri, iframeElement, figureId, model])
    useEffect(() => {

        function findAncestorElementWithClass(elmt: Element | undefined, className: string): Element | undefined {
            if (!elmt) return undefined
            if (elmt.className.split(' ').includes(className)) return elmt
            return findAncestorElementWithClass(elmt.parentElement || undefined, className)
        }
        function findDescendantElementWithClass(elmt: Element | undefined, className: string): Element | undefined {
            if (!elmt) return undefined
            if (elmt.className.split(' ').includes(className)) return elmt
            const childElements = elmt.children
            for (let i = 0; i < childElements.length; i++) {
                const childElement = childElements[i]
                const d = findDescendantElementWithClass(childElement, className)
                if (d) return d
            }
            return undefined
        }

        let canceled = false
        ;(async () => {
            let delay = 100 // start with a short delay and work up
            let lastWidth = 0
            while (!canceled) {
                // It is tricky to compute the width properly
                // After thoroughly inspecting the DOM, I think this is the best way
                const outputArea = findAncestorElementWithClass(iframeElement.current || undefined, 'jp-Cell-outputArea')
                const outputAreaPrompt = findDescendantElementWithClass(outputArea, 'jp-OutputArea-prompt')
                const W1 = outputArea?.getBoundingClientRect()?.width
                const W2 = outputAreaPrompt?.getBoundingClientRect()?.width
                if ((W1) && (W2)) {
                    const newWidth = W1 - W2
                    if (newWidth !== lastWidth) {
                        lastWidth = newWidth
                        delay = 500 // detect rapidly once again
                        setWidth(newWidth)
                    }
                }
                await sleepMsec(delay)
                delay += 100
                if (delay > 5000) delay = 5000
            }
        })()
        return () => {canceled = true}
    }, [iframeElement])
    const H = height || 400
    return (
        // important to use relative position rather than absolute (took me a while to figure that out)
        <div style={{ position: 'relative', width: width || 0, height: H, overflow: 'hidden' }}>
            <iframe
                ref={e => { iframeElement.current = e }}
                title="figure"
                src={src}
                width={width ? width - 15 : 0}
                height={H - 15}
            />
        </div>
    );
}

export default FigureWidget