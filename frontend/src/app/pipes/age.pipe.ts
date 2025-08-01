import { Pipe, PipeTransform } from "@angular/core";

@Pipe({
    name: 'age',
    standalone: true
})
export class AgePipe implements PipeTransform {
    transform(value: string) {
        const today = new Date();
        const birthDate = new Date(value);
        var age = today.getFullYear() - birthDate.getFullYear();
        const m = today.getMonth() - birthDate.getMonth();
        if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) { age--; }
        return age;
    }
}