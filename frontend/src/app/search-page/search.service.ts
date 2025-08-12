import { Injectable, signal } from "@angular/core";

@Injectable({
    providedIn: 'root'
})
export class SearchService {
    currPage = signal<number>(0);

    nextPage() {
        this.currPage.set(this.currPage() + 1)
    }

    prevPage() {
        this.currPage.set(Math.max(this.currPage() - 1, 0))
    }

    firstPage() {
        this.currPage.set(0)
    }

    goToPage(pageNum: number) {
        this.currPage.set(pageNum)
    }
}