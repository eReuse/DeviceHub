/*
 Copy and paste this in a Mongo shell.
 Returns the number of devices of the selected type in all the databases of the Mongo local instance.
 */
function getNumberOfDevicesInMongo (type) {
  var count = 0
  var mongo = db.getMongo()
  mongo.getDBs().databases.forEach(function (database) {
    var databaseName = database.name
    if (databaseName.indexOf('account') == -1) {
      count += mongo.getDB(databaseName)
      .getCollection('devices')
      .count({'@type': type})
    }
  })
  return count
}
getNumberOfDevicesInMongo('Computer')
