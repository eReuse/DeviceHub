from eve import Eve

app = Eve()
app.config.from_object('app.config')

from event_hooks import event_hooks
event_hooks(app)

if __name__ == '__main__':
    app.run()
