import express from 'express'
import { createClient } from 'redis'
import { promisify } from 'util'

const app = express()
const client = createClient()

const PORT = 1245

const listProducts = [
    { itemId: 1, itemName: 'Suitcase 250', price: 50, initialAvailableQuantity: 4 },
    { itemId: 2, itemName: 'Suitcase 450', price: 100, initialAvailableQuantity: 10 },
    { itemId: 3, itemName: 'Suitcase 650', price: 350, initialAvailableQuantity: 2 },
    { itemId: 4, itemName: 'Suitcase 1050', price: 550, initialAvailableQuantity: 5 }
]

const getItemById = (id) => {
    const foundId = listProducts.find(obj => obj.itemId === id)
    if (foundId) {
        return Object.fromEntries(Object.entries(foundId))
    }
}

/**
 * REDIS CLIENT CONNECTION
 * reserveStockById function
 * @param itemId
 * @param stock
 */

client.on('error', (errMessage) => {
        console.log(`Redis client not connected to the server:${errMessage.toString()}`)
    })
    /**
     * reserveStockById function
     * @param itemId
     * @param stock
     * @returns {*}
     */
const reserveStockById = (itemId, stock) => {
    //return promisify(client.get).bind(client)(`item.${itemId}`,stock)
    return client.set(stock, `item.${itemId}`)
}

/**
 *
 * @param itemId
 * @returns {Promise<*>}
 */

const get = promisify(client.get).bind(client)
const getCurrentReservedStockById = async(itemId) => {
    return await get(`item.${itemId}`)

}

client.on('connect', () => {
    console.log('Redis client connected to the server')
})


/**
 * @type express server connection config
 */
app.get('/', (_, res) => {
    res.send('Welcome Home homie')
})

app.get('/list_products', (req, res) => {
        res.json(listProducts)
    })
    // Product detail route
app.get('/list_products/:itemId(\\d+)', (req, res) => {
        const itemId = Number.parseInt(req.params.itemId)
        const foundItemId = getItemById(itemId)

        if (!foundItemId) res.json({ "status": 'Item not found!' })
        getCurrentReservedStockById(itemId)
            .then((resolve) => Number.parseInt(resolve || 0))
            .then((theReservedStock) => {
                foundItemId.currentQuantity = foundItemId.initialAvailableQuantity - theReservedStock
                res.json(foundItemId)
            })
    })
    // Reserve a product route
app.get('/reserve_product/:itemId', (req, res) => {
    const itemId = Number.parseInt(req.params.itemId)
    const foundItemId = getItemById(itemId)

    if (!foundItemId) return res.json({ status: "Product not found" })
    getCurrentReservedStockById(itemId)
        .then((result) => Number.parseInt(result || 0))
        .then((theReservedStock) => {
            if (theReservedStock >= foundItemId.initialAvailableQuantity) {
                return res.json({ status: `Not enough stock available,${itemId}` })
            }
            reserveStockById(itemId, theReservedStock + 1)
                // .then(() => {
                    return res.json({ status: `Reservation confirmed, ${itemId}` })
                //})
        })
})
const resetProductsStock = () => {
    return Promise.all(
        listProducts.map(
            item => promisify(client.set).bind(client)(`item.${item.itemId}`, 0),
        )
    );
};
app.listen(PORT, () => {
    resetProductsStock()
        .then(() => {
            console.log(`API available on localhost port ${PORT}`);
        });
})