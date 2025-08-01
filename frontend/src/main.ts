import { bootstrapApplication } from '@angular/platform-browser';
import { App } from './app/app';
import { HttpEventType, HttpHandlerFn, HttpRequest, provideHttpClient, withInterceptors } from '@angular/common/http';
import { tap } from 'rxjs';

function loggingInterceptor(request: HttpRequest<unknown>, next: HttpHandlerFn) {
  console.log('[Outgoing Request]');
  console.log(request);
  return next(request).pipe(
    tap({
      next: event => {
        if (event.type === HttpEventType.Response) {
          console.log('[Incoming Response]');
          console.log(event.status);
          console.log(event.body);
        }
      }
    })
  );
}

bootstrapApplication(App, {
  providers: [provideHttpClient(withInterceptors([loggingInterceptor]))]
})
  .catch((err) => console.error(err));
