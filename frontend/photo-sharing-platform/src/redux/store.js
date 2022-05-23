import { createStore, combineReducers } from 'redux'
import mainSearch from './reducers/search'
import imgDetail from './reducers/imgDetail'

const rootReducer = combineReducers({
    mainSearch,
    imgDetail
})

const store = createStore(rootReducer);
export default store