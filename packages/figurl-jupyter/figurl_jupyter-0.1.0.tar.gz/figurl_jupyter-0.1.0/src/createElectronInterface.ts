import { WidgetModel } from "@jupyter-widgets/base"
import deserializeReturnValue from "./deserializeReturnValue"
import { ElectronInterface } from "./FigInterface"
import QueryParameters from "./QueryParameters"
import { FigurlRequest, FigurlResponse } from "./viewInterface/FigurlRequestTypes"
import { TaskJobStatus, TaskType } from "./viewInterface/MessageToChildTypes"

const createElectronInterface = (model: WidgetModel): ElectronInterface => {

    let queryParameters: QueryParameters = {}

    const setQueryParameters = async (q: QueryParameters) => {
        queryParameters = q
    }

    const loadFileDataCallbacks: {[uri: string]: ((d: string) => void)[]} = {}
    const onFileData = (uri: string, callback: (d: string) => void) => {
        if (!loadFileDataCallbacks[uri]) loadFileDataCallbacks[uri] = []
        loadFileDataCallbacks[uri].push(callback)
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
    })

    async function loadFileData(uri: string) {
        model.send({type: 'loadFileDataRequest', uri}, () => {})
        return new Promise<any>((resolve, reject) => {
            onFileData(uri, (fileData: string) => {
                resolve(JSON.parse(fileData))
            })
        })
        
        const ret =JSON.parse(`{"autocorrelograms":[{"binCounts":{"_type":"ndarray","data_b64":"AwAAAAUAAAACAAAAAgAAAAAAAAACAAAABQAAAAQAAAACAAAABAAAAAQAAAAEAAAABAAAAAQAAAAFAAAABgAAAAYAAAAKAAAABwAAAAkAAAAJAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAkAAAAJAAAABwAAAAoAAAAGAAAABgAAAAUAAAAEAAAABAAAAAQAAAAEAAAABAAAAAIAAAAEAAAABQAAAAIAAAAAAAAAAgAAAAIAAAAFAAAAAwAAAA==","dtype":"int32","shape":[49]},"binEdgesSec":{"_type":"ndarray","data_b64":"ObTIvBKDwLzsUbi8xSCwvJ7vp7x3vp+8UI2XvClcj7wCK4e8tvN9vGiRbbwbL128zcxMvH9qPLwxCCy846UbvJZDC7yPwvW79P3Uu1g5tLu8dJO7QmBluwrXI7umm8S6bxIDum8SAzqmm8Q6CtcjO0JgZTu8dJM7WDm0O/T91DuPwvU7lkMLPOOlGzwxCCw8f2o8PM3MTDwbL108aJFtPLbzfTwCK4c8KVyPPFCNlzx3vp88nu+nPMUgsDzsUbg8EoPAPDm0yDw=","dtype":"float32","shape":[50]},"unitId":0},{"binCounts":{"_type":"ndarray","data_b64":"AQAAAAQAAAAEAAAAAQAAAAIAAAAFAAAABQAAAAMAAAAFAAAABAAAAAMAAAADAAAAAQAAAAYAAAADAAAABgAAAAIAAAAIAAAABQAAAAgAAAAOAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA4AAAAIAAAABQAAAAgAAAACAAAABgAAAAMAAAAGAAAAAQAAAAMAAAADAAAABAAAAAUAAAADAAAABQAAAAUAAAACAAAAAQAAAAQAAAAEAAAAAQAAAA==","dtype":"int32","shape":[49]},"binEdgesSec":{"_type":"ndarray","data_b64":"ObTIvBKDwLzsUbi8xSCwvJ7vp7x3vp+8UI2XvClcj7wCK4e8tvN9vGiRbbwbL128zcxMvH9qPLwxCCy846UbvJZDC7yPwvW79P3Uu1g5tLu8dJO7QmBluwrXI7umm8S6bxIDum8SAzqmm8Q6CtcjO0JgZTu8dJM7WDm0O/T91DuPwvU7lkMLPOOlGzwxCCw8f2o8PM3MTDwbL108aJFtPLbzfTwCK4c8KVyPPFCNlzx3vp88nu+nPMUgsDzsUbg8EoPAPDm0yDw=","dtype":"float32","shape":[50]},"unitId":1},{"binCounts":{"_type":"ndarray","data_b64":"AQAAAAQAAAACAAAABAAAAAcAAAAFAAAAAwAAAAMAAAADAAAABgAAAAUAAAAGAAAABAAAAAUAAAAIAAAAAwAAAAYAAAAFAAAABgAAAAkAAAAOAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA4AAAAJAAAABgAAAAUAAAAGAAAAAwAAAAgAAAAFAAAABAAAAAYAAAAFAAAABgAAAAMAAAADAAAAAwAAAAUAAAAHAAAABAAAAAIAAAAEAAAAAQAAAA==","dtype":"int32","shape":[49]},"binEdgesSec":{"_type":"ndarray","data_b64":"ObTIvBKDwLzsUbi8xSCwvJ7vp7x3vp+8UI2XvClcj7wCK4e8tvN9vGiRbbwbL128zcxMvH9qPLwxCCy846UbvJZDC7yPwvW79P3Uu1g5tLu8dJO7QmBluwrXI7umm8S6bxIDum8SAzqmm8Q6CtcjO0JgZTu8dJM7WDm0O/T91DuPwvU7lkMLPOOlGzwxCCw8f2o8PM3MTDwbL108aJFtPLbzfTwCK4c8KVyPPFCNlzx3vp88nu+nPMUgsDzsUbg8EoPAPDm0yDw=","dtype":"float32","shape":[50]},"unitId":2},{"binCounts":{"_type":"ndarray","data_b64":"BQAAAAMAAAABAAAABQAAAAQAAAADAAAAAwAAAAQAAAADAAAAAwAAAAQAAAAHAAAAAwAAAAYAAAADAAAACQAAAAYAAAAOAAAABQAAAA0AAAAPAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA8AAAANAAAABQAAAA4AAAAGAAAACQAAAAMAAAAGAAAAAwAAAAcAAAAEAAAAAwAAAAMAAAAEAAAAAwAAAAMAAAAEAAAABQAAAAEAAAADAAAABQAAAA==","dtype":"int32","shape":[49]},"binEdgesSec":{"_type":"ndarray","data_b64":"ObTIvBKDwLzsUbi8xSCwvJ7vp7x3vp+8UI2XvClcj7wCK4e8tvN9vGiRbbwbL128zcxMvH9qPLwxCCy846UbvJZDC7yPwvW79P3Uu1g5tLu8dJO7QmBluwrXI7umm8S6bxIDum8SAzqmm8Q6CtcjO0JgZTu8dJM7WDm0O/T91DuPwvU7lkMLPOOlGzwxCCw8f2o8PM3MTDwbL108aJFtPLbzfTwCK4c8KVyPPFCNlzx3vp88nu+nPMUgsDzsUbg8EoPAPDm0yDw=","dtype":"float32","shape":[50]},"unitId":3},{"binCounts":{"_type":"ndarray","data_b64":"BQAAAAYAAAAEAAAABQAAAAQAAAACAAAAAQAAAAIAAAADAAAABQAAAAMAAAAHAAAABQAAAAYAAAAFAAAABQAAAAMAAAAFAAAACwAAAAkAAAAKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAoAAAAJAAAACwAAAAUAAAADAAAABQAAAAUAAAAGAAAABQAAAAcAAAADAAAABQAAAAMAAAACAAAAAQAAAAIAAAAEAAAABQAAAAQAAAAGAAAABQAAAA==","dtype":"int32","shape":[49]},"binEdgesSec":{"_type":"ndarray","data_b64":"ObTIvBKDwLzsUbi8xSCwvJ7vp7x3vp+8UI2XvClcj7wCK4e8tvN9vGiRbbwbL128zcxMvH9qPLwxCCy846UbvJZDC7yPwvW79P3Uu1g5tLu8dJO7QmBluwrXI7umm8S6bxIDum8SAzqmm8Q6CtcjO0JgZTu8dJM7WDm0O/T91DuPwvU7lkMLPOOlGzwxCCw8f2o8PM3MTDwbL108aJFtPLbzfTwCK4c8KVyPPFCNlzx3vp88nu+nPMUgsDzsUbg8EoPAPDm0yDw=","dtype":"float32","shape":[50]},"unitId":4},{"binCounts":{"_type":"ndarray","data_b64":"BQAAAAgAAAACAAAAAgAAAAQAAAAEAAAABAAAAAMAAAAEAAAABwAAAAQAAAAEAAAAAwAAAAQAAAACAAAABQAAAAkAAAAFAAAABQAAAAkAAAAKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAoAAAAJAAAABQAAAAUAAAAJAAAABQAAAAIAAAAEAAAAAwAAAAQAAAAEAAAABwAAAAQAAAADAAAABAAAAAQAAAAEAAAAAgAAAAIAAAAIAAAABQAAAA==","dtype":"int32","shape":[49]},"binEdgesSec":{"_type":"ndarray","data_b64":"ObTIvBKDwLzsUbi8xSCwvJ7vp7x3vp+8UI2XvClcj7wCK4e8tvN9vGiRbbwbL128zcxMvH9qPLwxCCy846UbvJZDC7yPwvW79P3Uu1g5tLu8dJO7QmBluwrXI7umm8S6bxIDum8SAzqmm8Q6CtcjO0JgZTu8dJM7WDm0O/T91DuPwvU7lkMLPOOlGzwxCCw8f2o8PM3MTDwbL108aJFtPLbzfTwCK4c8KVyPPFCNlzx3vp88nu+nPMUgsDzsUbg8EoPAPDm0yDw=","dtype":"float32","shape":[50]},"unitId":5},{"binCounts":{"_type":"ndarray","data_b64":"BAAAAAYAAAAEAAAABAAAAAIAAAABAAAAAQAAAAEAAAAGAAAAAgAAAAMAAAAFAAAAAwAAAAEAAAAIAAAAAgAAAAQAAAAGAAAACwAAAAcAAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAHAAAACwAAAAYAAAAEAAAAAgAAAAgAAAABAAAAAwAAAAUAAAADAAAAAgAAAAYAAAABAAAAAQAAAAEAAAACAAAABAAAAAQAAAAGAAAABAAAAA==","dtype":"int32","shape":[49]},"binEdgesSec":{"_type":"ndarray","data_b64":"ObTIvBKDwLzsUbi8xSCwvJ7vp7x3vp+8UI2XvClcj7wCK4e8tvN9vGiRbbwbL128zcxMvH9qPLwxCCy846UbvJZDC7yPwvW79P3Uu1g5tLu8dJO7QmBluwrXI7umm8S6bxIDum8SAzqmm8Q6CtcjO0JgZTu8dJM7WDm0O/T91DuPwvU7lkMLPOOlGzwxCCw8f2o8PM3MTDwbL108aJFtPLbzfTwCK4c8KVyPPFCNlzx3vp88nu+nPMUgsDzsUbg8EoPAPDm0yDw=","dtype":"float32","shape":[50]},"unitId":6},{"binCounts":{"_type":"ndarray","data_b64":"AQAAAAIAAAAFAAAABwAAAAUAAAACAAAABwAAAAMAAAAJAAAABgAAAAMAAAADAAAABAAAAAYAAAACAAAABAAAAAIAAAAFAAAABwAAAA0AAAALAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAsAAAANAAAABwAAAAUAAAACAAAABAAAAAIAAAAGAAAABAAAAAMAAAADAAAABgAAAAkAAAADAAAABwAAAAIAAAAFAAAABwAAAAUAAAACAAAAAQAAAA==","dtype":"int32","shape":[49]},"binEdgesSec":{"_type":"ndarray","data_b64":"ObTIvBKDwLzsUbi8xSCwvJ7vp7x3vp+8UI2XvClcj7wCK4e8tvN9vGiRbbwbL128zcxMvH9qPLwxCCy846UbvJZDC7yPwvW79P3Uu1g5tLu8dJO7QmBluwrXI7umm8S6bxIDum8SAzqmm8Q6CtcjO0JgZTu8dJM7WDm0O/T91DuPwvU7lkMLPOOlGzwxCCw8f2o8PM3MTDwbL108aJFtPLbzfTwCK4c8KVyPPFCNlzx3vp88nu+nPMUgsDzsUbg8EoPAPDm0yDw=","dtype":"float32","shape":[50]},"unitId":7},{"binCounts":{"_type":"ndarray","data_b64":"AAAAAAYAAAAEAAAAAgAAAAMAAAAEAAAABgAAAAQAAAAHAAAAAwAAAAUAAAAHAAAAAwAAAAcAAAAHAAAAAgAAAAcAAAAGAAAACAAAAAcAAAAGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAYAAAAHAAAACAAAAAYAAAAHAAAAAgAAAAcAAAAHAAAAAwAAAAcAAAAFAAAAAwAAAAcAAAAEAAAABgAAAAQAAAADAAAAAgAAAAQAAAAGAAAAAAAAAA==","dtype":"int32","shape":[49]},"binEdgesSec":{"_type":"ndarray","data_b64":"ObTIvBKDwLzsUbi8xSCwvJ7vp7x3vp+8UI2XvClcj7wCK4e8tvN9vGiRbbwbL128zcxMvH9qPLwxCCy846UbvJZDC7yPwvW79P3Uu1g5tLu8dJO7QmBluwrXI7umm8S6bxIDum8SAzqmm8Q6CtcjO0JgZTu8dJM7WDm0O/T91DuPwvU7lkMLPOOlGzwxCCw8f2o8PM3MTDwbL108aJFtPLbzfTwCK4c8KVyPPFCNlzx3vp88nu+nPMUgsDzsUbg8EoPAPDm0yDw=","dtype":"float32","shape":[50]},"unitId":8},{"binCounts":{"_type":"ndarray","data_b64":"AwAAAAIAAAABAAAABAAAAAQAAAAFAAAAAgAAAAMAAAAGAAAAAwAAAAMAAAACAAAAAwAAAAYAAAAGAAAABgAAAAIAAAAHAAAABwAAAAgAAAAKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAoAAAAIAAAABwAAAAcAAAACAAAABgAAAAYAAAAGAAAAAwAAAAIAAAADAAAAAwAAAAYAAAADAAAAAgAAAAUAAAAEAAAABAAAAAEAAAACAAAAAwAAAA==","dtype":"int32","shape":[49]},"binEdgesSec":{"_type":"ndarray","data_b64":"ObTIvBKDwLzsUbi8xSCwvJ7vp7x3vp+8UI2XvClcj7wCK4e8tvN9vGiRbbwbL128zcxMvH9qPLwxCCy846UbvJZDC7yPwvW79P3Uu1g5tLu8dJO7QmBluwrXI7umm8S6bxIDum8SAzqmm8Q6CtcjO0JgZTu8dJM7WDm0O/T91DuPwvU7lkMLPOOlGzwxCCw8f2o8PM3MTDwbL108aJFtPLbzfTwCK4c8KVyPPFCNlzx3vp88nu+nPMUgsDzsUbg8EoPAPDm0yDw=","dtype":"float32","shape":[50]},"unitId":9},{"binCounts":{"_type":"ndarray","data_b64":"BQAAAAEAAAAAAAAAAwAAAAIAAAAFAAAAAgAAAAUAAAACAAAABgAAAAcAAAADAAAAAgAAAAIAAAALAAAABAAAAAcAAAAKAAAAAwAAAAsAAAALAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAsAAAALAAAAAwAAAAoAAAAHAAAABAAAAAsAAAACAAAAAgAAAAMAAAAHAAAABgAAAAIAAAAFAAAAAgAAAAUAAAACAAAAAwAAAAAAAAABAAAABQAAAA==","dtype":"int32","shape":[49]},"binEdgesSec":{"_type":"ndarray","data_b64":"ObTIvBKDwLzsUbi8xSCwvJ7vp7x3vp+8UI2XvClcj7wCK4e8tvN9vGiRbbwbL128zcxMvH9qPLwxCCy846UbvJZDC7yPwvW79P3Uu1g5tLu8dJO7QmBluwrXI7umm8S6bxIDum8SAzqmm8Q6CtcjO0JgZTu8dJM7WDm0O/T91DuPwvU7lkMLPOOlGzwxCCw8f2o8PM3MTDwbL108aJFtPLbzfTwCK4c8KVyPPFCNlzx3vp88nu+nPMUgsDzsUbg8EoPAPDm0yDw=","dtype":"float32","shape":[50]},"unitId":10},{"binCounts":{"_type":"ndarray","data_b64":"AwAAAAMAAAACAAAAAgAAAAYAAAADAAAAAwAAAAIAAAAHAAAAAwAAAAMAAAACAAAABgAAAAUAAAAFAAAAAwAAAAQAAAALAAAABgAAAAkAAAAKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAoAAAAJAAAABgAAAAsAAAAEAAAAAwAAAAUAAAAFAAAABgAAAAIAAAADAAAAAwAAAAcAAAACAAAAAwAAAAMAAAAGAAAAAgAAAAIAAAADAAAAAwAAAA==","dtype":"int32","shape":[49]},"binEdgesSec":{"_type":"ndarray","data_b64":"ObTIvBKDwLzsUbi8xSCwvJ7vp7x3vp+8UI2XvClcj7wCK4e8tvN9vGiRbbwbL128zcxMvH9qPLwxCCy846UbvJZDC7yPwvW79P3Uu1g5tLu8dJO7QmBluwrXI7umm8S6bxIDum8SAzqmm8Q6CtcjO0JgZTu8dJM7WDm0O/T91DuPwvU7lkMLPOOlGzwxCCw8f2o8PM3MTDwbL108aJFtPLbzfTwCK4c8KVyPPFCNlzx3vp88nu+nPMUgsDzsUbg8EoPAPDm0yDw=","dtype":"float32","shape":[50]},"unitId":11}],"type":"Autocorrelograms"}`)
        // don't deserialize here because Buffer behaves differently in electron
        return ret
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
        else return undefined
    }
    return {
        setQueryParameters,
        handleFigurlRequest,
        onTaskStatusUpdate: (callback: (a: {taskType: TaskType, taskName: string, taskJobId: string, status: TaskJobStatus, errorMessage?: string}) => void) => {},
        getTaskReturnValue: async (a: {taskName: string, taskJobId: string}): Promise<any | undefined> => {}
    }
}

export default createElectronInterface