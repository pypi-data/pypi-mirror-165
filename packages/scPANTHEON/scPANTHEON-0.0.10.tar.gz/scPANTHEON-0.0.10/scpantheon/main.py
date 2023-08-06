import source
# from bokeh.server.server import Server

# server = Server({'/': source.main}, num_procs=4)
# server.start()

# if __name__ == '__main__':
#     print('Opening Bokeh application on http://localhost:5006/')

#     server.io_loop.add_callback(server.show, "/")
#     server.io_loop.start()

source.main()