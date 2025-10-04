import { Injectable, signal, computed } from "@angular/core";

export type SortDirection = 'asc' | 'desc' | null;

export interface SortConfig<T> {
    [key: string]: (item: T) => number;
}

@Injectable()
export class TableSortService<T> {
    private sortState = signal<{column: string | null, direction: SortDirection}>({
        column: null,
        direction: null
    })

    private sortConfig = signal<SortConfig<T> | null>(null);
    private data = signal<T[]>([]);
    
    setSortConfig(config: SortConfig<T>) {
        this.sortConfig.set(config);
    }

    setData(data: T[]) {
        this.data.set(data)
    }

    sortedData = computed(() => {
        if (!this.sortState().column || !this.sortState().direction || !this.sortConfig()) {
            return this.data();
        }

        // Function that gets corresponding value to sort by from object
        const getValue = this.sortConfig()![this.sortState().column!];
        if (!getValue) {
            return this.data();
        }

        return this.data().sort((a,b) => {
            const valueA = getValue(a);
            const valueB = getValue(b);

            if (this.sortState().direction === 'asc') {
                return valueA - valueB;
            } else {
                return valueB - valueA;
            }
        })
    })

    toggleSort(column: string) {
        if (this.sortState().column === column) {
            // Cycle through desc -> asc -> null -> desc
            if (this.sortState().direction === 'desc') {
                this.sortState.set({column, direction: 'asc'});
            } else if (this.sortState().direction === 'asc') {
                this.sortState.set({column, direction: 'desc'});
            } else {
                this.sortState.set({column, direction: 'desc'});
            }
        } else {
            this.sortState.set({column, direction: 'desc'})
        }
    }

    getSortIcon(column: string): string {
        const direction = this.sortState().column === column ? this.sortState().direction : null;
        switch (direction) {
            case 'asc': return '↑';
            case 'desc': return '↓';
            default: return '';
        }
    }
}