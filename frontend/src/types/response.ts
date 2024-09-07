declare namespace Api {
    interface Response<T> {
        success: true,
        data: T
    }

    interface Error<T> {
        success: true,
        message: string
    }

    interface Sample {
        id: number,
        title: string | null,
        artist: string | null,
        album: string | null,
        is_processed: boolean,
        sha256: string,
    }
}