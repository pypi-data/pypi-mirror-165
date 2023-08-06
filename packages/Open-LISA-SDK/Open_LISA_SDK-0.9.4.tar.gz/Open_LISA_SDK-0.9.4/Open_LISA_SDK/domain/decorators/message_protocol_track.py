from ...domain.exceptions.sdk_exception import OpenLISAException
from ...common.utils.bytes import format_bytes
from ...logging import log


def with_message_protocol_track_log(method):
    def inner(ref, *args, **kwargs):
        ref._message_protocol.start_track()
        method_result = method(ref, *args, **kwargs)
        track = ref._message_protocol.get_track()
        method_name = method.__name__.replace("_as_json_string", "")
        total_bytes = track.bytes_sent + track.bytes_received
        elapsed = track.finish_timestamp - track.begin_timestamp
        if elapsed == 0:
            elapsed = 0.0000001
        throughput = total_bytes / elapsed
        log.debug("[LATENCY][method={}][communication_protocol={}][elapsed_time={:.2f} seconds][sent={}][received={}][total_transferred_bytes={}][throughput={}/s]".format(
            method_name,
            track.protocol,
            track.finish_timestamp - track.begin_timestamp,
            format_bytes(track.bytes_sent),
            format_bytes(track.bytes_received),
            format_bytes(total_bytes),
            format_bytes(throughput)
        ))
        return method_result
    return inner


def with_message_protocol_track(output):
    if output == "LOG":
        return with_message_protocol_track_log
    # NOTE: here more outputs could be supported. Examples: excel, filesystem, etc.
    else:
        raise OpenLISAException(
            "with_message_protocol_track decorator was init with invalid output {}".format(output))
