ID00 = '<ID00>'
ID01 = '<ID01>'
ID02 = '<ID02>'

WAIT_1S = '<WB>'
WAIT_2S = '<WC>'
WAIT_3S = '<WD>'
WAIT_4S = '<WE>'
WAIT_5S = '<WF>'

COLOR_RED = '<CA>'
COLOR_GREEN = '<CD>'
COLOR_AMBER = '<CH>'
COLOR_RAG = '<CR>'

FUNCTION_SPEED_1 = '<FX>'
FUNCTION_SPEED_2 = '<FY>'
FUNCTION_SPEED_3 = '<FZ>'

SCROLL_LEFT = '<FE>'


def checksum(buffer):
    checksum_i = int(0)

    for element in buffer:
        element_i = ord(element)
        checksum_i ^= element_i
    return checksum_i


def init_id(id_number):
    display_buffer = '<ID>{id_number}<E>'.format(id_number=id_number)
    return display_buffer


#
#   delete_all:
#
def delete_all(id):
    def data_packet():
        checksum_buffer = '<D*>'
        return checksum_buffer

    cs = checksum(data_packet())
    display_buffer = '{id}{data_packet}{cs:02X}<E>'.format(
        id=id
        , data_packet=data_packet()
        , cs=cs
    )
    return display_buffer


#
#   delete_page:
#
def delete_page(id, page_id, line):
    def data_packet(page, line):
        checksum_buffer = '<D{line}XP{page_id}>'.format(page_id=page_id, line=line)
        return checksum_buffer

    cs = checksum(data_packet(page_id, line))
    display_buffer = '{id}{data_packet}{cs:02X}<E>'.format(
        id=id
        , data_packet=data_packet(page_id, line)
        , cs=cs
    )
    return display_buffer


#
#   link_pages:
#       tell Vellemann Display which programmed pages to show
#
def link_pages(id, pages):
    def data_packet(pages):
        checksum_buffer = '<TA>00010100009912312359{pages}'.format(pages=pages)
        return checksum_buffer

    cs = checksum(data_packet(pages))
    display_buffer = '{id}{data_packet}{cs:02X}<E>'.format(
        id=id
        , data_packet=data_packet(pages)
        , cs=cs
    )
    return display_buffer


#
#   display_page
#       define a Page within Vellemann Display
#
def send_page(id, line_id, page_id, color, wait, request):
    def data_packet(line_id, page_id, color, wait, request):
        checksum_buffer = '<L{line_id}><P{page_id}><FE><MA>{wait}{lagging_command}{color}{request}'.format(
            line_id=line_id
            , page_id=page_id
            , wait=wait
            , lagging_command=SCROLL_LEFT
            , color=color
            , request=request
        )
        return checksum_buffer

    cs = checksum(data_packet(line_id, page_id, color, wait, request))
    display_buffer = '{id}{data_packet}{cs:02X}<E>'.format(
        id=id
        , data_packet=data_packet(line_id, page_id, color, wait, request)
        , cs=cs
    )
    return display_buffer
