import chunkfile


def main():
    cgf = chunkfile.load_chunk_file(
        r"D:\perforce\dev\GameSDK\Objects\basebuilding\wood\wood_gallow.cgf"
    )

    # Iterate through the chunks in a chunkfile
    for chunk in cgf.iter_chunks():
        print(chunk[0])
        print(type(chunk[0]))

        # get the Physics data from a Mesh Chunk
        if type(chunk[0]) is chunkfile.mesh_chunk.MeshChunk:
            reader = chunkfile.chunk.DataReader(chunk[0].data)
            header = chunk[0].read_header_801(reader)
            print(header.find_field("nPhysicsDataChunk").value)
        print(dir(chunk[0].format(0)))

        print(chunk[0].data)


if __name__ == "__main__":
    main()
