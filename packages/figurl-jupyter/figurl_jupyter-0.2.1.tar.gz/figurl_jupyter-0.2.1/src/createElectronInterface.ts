import { WidgetModel } from "@jupyter-widgets/base"
import deserializeReturnValue from "./deserializeReturnValue"
import { ElectronInterface } from "./FigInterface"
import QueryParameters from "./QueryParameters"
import randomAlphaString from "./util/randomAlphaString"
import { FigurlRequest, FigurlResponse, InitiateTaskResponse } from "./viewInterface/FigurlRequestTypes"
import { sha1OfObject, sha1OfString } from "./viewInterface/kacheryTypes"
import { TaskJobStatus, TaskType } from "./viewInterface/MessageToChildTypes"

const createElectronInterface = (model: WidgetModel): ElectronInterface => {

    let queryParameters: QueryParameters = {}

    const setQueryParameters = async (q: QueryParameters) => {
        queryParameters = q
    }

    const taskStatusUpdateCallbacks: ((a: {taskType: TaskType, taskName: string, taskJobId: string, status: TaskJobStatus, errorMessage?: string}) => void)[] = []

    const loadFileDataCallbacks: {[uri: string]: ((d: string | undefined) => void)[]} = {}
    const onFileData = (uri: string, callback: (d: string | undefined) => void) => {
        if (!loadFileDataCallbacks[uri]) loadFileDataCallbacks[uri] = []
        loadFileDataCallbacks[uri].push(callback)
    }
    const loadTaskReturnValueCallbacks: {[key: string]: ((d: string | undefined) => void)[]} = {}
    const onTaskReturnValue = (o: {taskName: string, taskJobId: string}, callback: (d: string | undefined) => void) => {
        const {taskName, taskJobId} = o
        const key = `${taskName}.${taskJobId}`
        if (!loadTaskReturnValueCallbacks[key]) loadTaskReturnValueCallbacks[key] = []
        loadTaskReturnValueCallbacks[key].push(callback)
    }
    model.on('msg:custom', msg => {
        console.info('Message from python', msg)
        if (msg.type === 'loadFileDataResponse') {
            const {fileData, uri} = msg
            const callbacks = loadFileDataCallbacks[uri]
            if (callbacks) {
                loadFileDataCallbacks[uri] = []
                for (let cb of callbacks) {
                    cb(fileData)
                }
            }
        }
        else if (msg.type === 'loadTaskReturnValueResponse') {
            const {data, taskName, taskJobId} = msg
            const key = `${taskName}.${taskJobId}`
            const callbacks = loadTaskReturnValueCallbacks[key]
            if (callbacks) {
                loadTaskReturnValueCallbacks[key] = []
                for (let cb of callbacks) {
                    cb(data)
                }
            }
        }
        else if (msg.type === 'taskStatusUpdate') {
            const {taskType, taskName, taskJobId, status, error} = msg as {taskType: TaskType, taskName: string, taskJobId: string, status: TaskJobStatus, error: string | undefined}
            for (let cb of taskStatusUpdateCallbacks) {
                cb({taskType, taskName, taskJobId, status, errorMessage: error})
            }
        }
    })

    async function loadFileData(uri: string) {
        model.send({type: 'loadFileDataRequest', uri}, () => {})
        return new Promise<string | undefined>((resolve, reject) => {
            onFileData(uri, (fileData: string | undefined) => {
                resolve(fileData ? JSON.parse(fileData) : undefined)
            })
        })
    }

    async function getTaskReturnValue(o: {taskName: string, taskJobId: string}) {
        const {taskName, taskJobId} = o
        model.send({type: 'loadTaskReturnValue', taskName, taskJobId}, () => {})
        return new Promise<string | undefined>((resolve, reject) => {
            onTaskReturnValue({taskName, taskJobId}, (data: string | undefined) => {
                resolve(data ? JSON.parse(data) : undefined)
            })
        })
    }

    const handleFigurlRequest = async (req: FigurlRequest): Promise<FigurlResponse | undefined> => {
        if (req.type === 'getFigureData') {
            if (!queryParameters.dataUri) throw Error('dataUri is not set in preload.ts')
            const figureData = await loadFileData(queryParameters.dataUri)
            return {
                type: 'getFigureData',
                figureData
            }
        }
        else if (req.type === 'getFileData') {
            const fileData = await loadFileData(req.uri)
            return {
                type: 'getFileData',
                fileData
            }
        }
        else if (req.type === 'initiateTask') {
            const {taskInput, taskName, taskType} = req
            const taskJobId = taskType === 'calculation' ? (
                sha1OfObject({taskName, taskInput})
            ) : (
                sha1OfString(randomAlphaString(100))
            )

            if (taskType === 'calculation') {
                // see if already finished
                const returnValue = await getTaskReturnValue({taskName, taskJobId: taskJobId.toString()})
                if (returnValue !== undefined) {
                    // already finished, no pubsub needed
                    return {
                        type: 'initiateTask',
                        taskJobId: taskJobId.toString(),
                        status: 'finished',
                        returnValue
                    }
                }
            }

            model.send({type: 'requestTask', taskType, taskName, taskInput, taskJobId}, () => {})

            const ret: InitiateTaskResponse = {
                type: 'initiateTask',
                taskJobId: taskJobId.toString(),
                status: 'waiting'
            }
            return ret
        }
        else return undefined
    }
    const onTaskStatusUpdate = (callback: (a: {taskType: TaskType, taskName: string, taskJobId: string, status: TaskJobStatus, errorMessage?: string}) => void) => {
        taskStatusUpdateCallbacks.push(callback)
    }
    return {
        setQueryParameters,
        handleFigurlRequest,
        onTaskStatusUpdate,
        getTaskReturnValue
    }
}

export default createElectronInterface