<script lang="ts">
    import { PUBLIC_VERSION, PUBLIC_COMMIT_HASH } from '$env/static/public'
</script>

<!--@component
Simple component to display version info. Relies on the environment variables PUBLIC_VERSION and
PUBLIC_COMMIT_HASH to work. so that's maybe... bad.
-->
<span class="inline-block px-2">
    <b>v{PUBLIC_VERSION}</b> on
    <span class="hoverable group">
        <a href={`http://www.github.com/bustosalex1/ae8900/tree/${PUBLIC_COMMIT_HASH}`}>
            <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 16 16"
                width="16"
                height="16"
                class="fill-base-content inline-block align-text-top group-hover:fill-primary transition ease-in-out duration-300"
                ><path
                    d="M9.5 3.25a2.25 2.25 0 1 1 3 2.122V6A2.5 2.5 0 0 1 10 8.5H6a1 1 0 0 0-1 1v1.128a2.251 2.251 0 1 1-1.5 0V5.372a2.25 2.25 0 1 1 1.5 0v1.836A2.493 2.493 0 0 1 6 7h4a1 1 0 0 0 1-1v-.628A2.25 2.25 0 0 1 9.5 3.25Zm-6 0a.75.75 0 1 0 1.5 0 .75.75 0 0 0-1.5 0Zm8.25-.75a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5ZM4.25 12a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Z"
                /></svg
            >
            <b>
                {PUBLIC_COMMIT_HASH}
            </b>
        </a>
    </span>
</span>
